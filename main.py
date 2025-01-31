import functools
import os
from threading import Thread
from evaluation import evaluation_execution_loop
from introspection import get_neo4j_metadata
from generate_prompt import SystemPrompt, UserPrompt
from ollama import chat
from ollama import ChatResponse
from drivers.dataloader import download_neo4j_text2cypher
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai import GenerativeModel
from pandas import DataFrame
from typing import Union
from time import sleep
from drivers.loadenv import load_env
from loguru import logger

import csv
import pika
from pika.adapters.blocking_connection import BlockingChannel
from constants.globalconstant import *
from pathlib import Path


def validate_queue(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        channel = kwargs.get('channel')
        channel.queue_declare(queue=MESSAGE_QUEUE_EVAL)
        return func(*args, **kwargs)
    return wrapper


@validate_queue
def generate_cypher_queries(data: DataFrame, 
                            prompt: Union[UserPrompt, SystemPrompt], 
                            model: GenerativeModel,
                            channel: BlockingChannel) -> dict:
    
    
    # Build prompts to generate required Cypher queries
    for index, row in data.iterrows():
        try:

            nlp_query = row["question"]
            db_schema = row["schema"]
            ground_truth = row["cypher"]
            unique_id = row["instance_id"]

            user_prompt = prompt.create_prompt_builder().build_prompt(
            role="user",
            context=str(nlp_query),
            input_data=str(db_schema)
            )

            message_user = {
                "role": user_prompt['role'], 
                'content': {
                    "Task": user_prompt['context'],
                    "Instructions": "Use only the provided relationship types and properties. \
                        Do not use any other relationship types or properties that are not provided. \
                        Return just the cypher query inside three quotes and nothing else. \
                        If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.",
                    "Schema": str(user_prompt['input_data'])
                }
            }
            response = model.generate_content(str(message_user))
            CYPHER_QUERY_PAIRS.update({unique_id: {"unique_id": unique_id, 
                                                "nlp_query": user_prompt["context"],
                                                "real": ground_truth,
                                                "generated": str(response.text).replace("\n", " ").replace("```cypher", " ")
                                                }
                                    }
                                )
            # logger.info(CYPHER_QUERY_PAIRS)

            # Add the new query to the queue for the evaluation process
            channel.basic_publish(exchange='',
                                routing_key=MESSAGE_QUEUE_EVAL,
                                body=unique_id)
            
            if (index+1) % GOOGLE_PER_MIN_QUOTA == 0:
                # Evaluate generated cyphers
                # evaluate_generated_cyphers(index)
                sleep(60)
            
            if index == GOOGLE_REQUEST_QUOTA:
                channel.basic_publish(exchange='',
                                routing_key=MESSAGE_QUEUE_EVAL,
                                body=CLOSE_MESSAGING)
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
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    return channel, connection

def save_results() -> None:
    file_path = Path(os.getcwd(),"result.csv")
    if file_path.exists():
       file_path.unlink()
    
    try:
        # Save results
        with open("result.csv", 'w') as file:
            wr = csv.writer(file)
            wr.writerow(["nlp_query", "real", "generated", "score"])

            for row in CYPHER_QUERY_PAIRS:
                wr.writerow([CYPHER_QUERY_PAIRS[row]["nlp_query"], 
                            CYPHER_QUERY_PAIRS[row]["real"], 
                            CYPHER_QUERY_PAIRS[row]["generated"], 
                            CYPHER_QUERY_PAIRS[row]["score"]
                            ])  
    except KeyError:
        pass
    

def execution_loop():
    # Load the environment
    load_env()

    # Establish a connection RabbitMQ server
    channel, connection = connect_rabbitmq_server()
    CONNECTION_INFO["publisher"] = {"channel": channel, "connection": connection}

    # Configure LLM API
    model = configure_llm()

    # Download data
    data = download_neo4j_text2cypher()
    logger.info(data.head)

    # Run evaluation loop
    thread = Thread(target=evaluation_execution_loop)
    thread.start()

    # Generate cypher queries
    generate_cypher_queries(data=data, prompt=UserPrompt(), model=model, channel=channel)

    thread.join()

    save_results()

    # Close the connection for the publisher
    CONNECTION_INFO["publisher"]["connection"].close()   


if __name__ == "__main__":
    execution_loop()