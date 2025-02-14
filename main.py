import functools
import os
from tqdm import tqdm
from threading import Thread
from drivers.csvhandler import CSVHandler
from evaluation import evaluation_execution_loop
from neo4jam.introspection import get_neo4j_metadata
from neo4jam.data.generate_prompt import SystemPrompt, UserPrompt
from ollama import chat
from ollama import ChatResponse
from drivers.dataloader import download_neo4j_text2cypher
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai import GenerativeModel
from pandas import DataFrame
from typing import Union
from time import sleep
from neo4jam.loadenv import load_env
from loguru import logger

import csv
import pika
from pika.adapters.blocking_connection import BlockingChannel
from constants.globalconstant import *
from pathlib import Path

CYPHER_QUERY_PAIRS = []
GOOGLE_REQUEST_QUOTA = 15
GOOGLE_PER_MIN_QUOTA = 15
MESSAGE_QUEUE_EVAL = "evaluate"
CLOSE_MESSAGING = "close"
CONNECTION_INFO = {}


def generate_cypher_queries(
    data: DataFrame, prompt: Union[UserPrompt, SystemPrompt], model: GenerativeModel
) -> dict:

    # Build prompts to generate required Cypher queries
    for index, row in data.iterrows():
        logger.info("Processing row: {}", index)

        try:
            nlp_query = row["question"]
            db_schema = row["schema"]
            ground_truth = row["cypher"]
            unique_id = row["instance_id"]
            database_reference = row["database_reference_alias"]

            user_prompt = prompt.create_prompt_builder().build_prompt(
                role="user", context=str(nlp_query), input_data=str(db_schema)
            )

            message_user = {
                "role": user_prompt["role"],
                "content": {
                    "Task": user_prompt["context"],
                    "Instructions": "Use only the provided relationship types and properties. \
                        Do not use any other relationship types or properties that are not provided. \
                        Return just the cypher query inside three quotes and nothing else. \
                        If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.",
                    "Schema": str(user_prompt["input_data"]),
                },
            }
            response = model.generate_content(str(message_user))
            CYPHER_QUERY_PAIRS.append(
                {                    
                    "unique_id": unique_id,
                    "nlp_query": user_prompt["context"],
                    "database_reference": database_reference,
                    "real": ground_truth,
                    "generated": str(response.text)
                    .replace("\n", " ")
                    .replace("```cypher", " ")
                    .replace("```", " "),                    
                }
            )
            # logger.info(CYPHER_QUERY_PAIRS)

            # # Add the new query to the queue for the evaluation process
            # channel.basic_publish(
            #     exchange="", routing_key=MESSAGE_QUEUE_EVAL, body=unique_id
            # )

            if (index + 1) % GOOGLE_PER_MIN_QUOTA == 0:
                # Evaluate generated cyphers
                # evaluate_generated_cyphers(index)
                sleep(60)

            if index == GOOGLE_REQUEST_QUOTA:
                logger.warning("Google request quota reached. Exiting...")
                # channel.basic_publish(
                #     exchange="", routing_key=MESSAGE_QUEUE_EVAL, body=CLOSE_MESSAGING
                # )
                return
        except ResourceExhausted:
            sleep(60)
            continue


def configure_llm() -> GenerativeModel:
    # Configure Gemini API
    genai.configure(api_key=os.getenv("GEMINI"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def connect_rabbitmq_server() -> BlockingChannel:
    parameters = pika.ConnectionParameters(
        host="localhost",
        port=5672,
        heartbeat=600,  # Increase heartbeat
        blocked_connection_timeout=300,
    )
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    return channel, connection

def save_results_to_csv():
    csv_handler = CSVHandler(RESULT_FILE_PATH, INPUT_COLUMNS)
    csv_handler.save_list_to_csv(CYPHER_QUERY_PAIRS)


def execution_loop():
    # Load the environment
    load_env()

    # # Establish a connection RabbitMQ server
    # channel, connection = connect_rabbitmq_server()
    # CONNECTION_INFO["publisher"] = {"channel": channel, "connection": connection}

    # Configure LLM API
    model = configure_llm()

    # Download data
    data = download_neo4j_text2cypher()
    logger.info(data.head(5))

    # # Run evaluation loop
    # thread = Thread(target=evaluation_execution_loop)
    # thread.start()

    # Generate cypher queries
    generate_cypher_queries(data=data, prompt=UserPrompt(), model=model)
    save_results_to_csv()

    # thread.join()

    # Close the connection for the publisher
    # CONNECTION_INFO["publisher"]["connection"].close()
    # CONNECTION_INFO["publisher"]["channel"].queue_delete(queue=MESSAGE_QUEUE_EVAL)


if __name__ == "__main__":
    execution_loop()
