# This module is responsible for generating Cypher queries for Neo4j database with the help of a LLM.

import os
import sys
from time import sleep
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame
from pathlib import Path
import pandas as pd

# Add the directory containing generate_prompt.py to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from generate_prompt import SystemPrompt, UserPrompt
from google.generativeai import GenerativeModel
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai

GOOGLE_REQUEST_QUOTA = 15
GOOGLE_PER_MIN_QUOTA = 15


# TODO: Configure the LLM model passed in the function
def configure_llm() -> GenerativeModel:
    # Configure Gemini API
    genai.configure(api_key=os.getenv("GEMINI"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def generate_cypher_queries(
    dataframe: DataFrame,
    prompt: Union[UserPrompt, SystemPrompt],
    model: GenerativeModel,
) -> dict:
    # Build prompts to generate required Cypher queries
    for index, row in dataframe.iterrows():
        logger.info("Processing row: {}", row["instance_id"])

        try:
            nlp_query = row["question"]
            db_schema = row["schema"]

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

            # Process the generated response
            response = (
                str(response.text)
                .replace("\n", " ")
                .replace("```cypher", " ")
                .replace("```", " ")
            )

            # Update the dataframe with the generated response
            dataframe.at[index, "generated"] = response
            
            if (index + 1) % GOOGLE_PER_MIN_QUOTA == 0:
                sleep(60)

            if index == GOOGLE_REQUEST_QUOTA:
                logger.warning("Google request quota reached. Exiting...")
                return dataframe
        except ResourceExhausted:
            sleep(60)
            continue
    return dataframe


# Method to load CSV files from a directory
def fetch_data_from_dir(directory: str) -> Generator[tuple[str, DataFrame], None, None]:
    """Fetches data from all CSV files in a directory and returns a DataFrame."""
    for file in Path(directory).rglob("*.csv"):
        try:
            filename = ".".join([file.stem, file.suffix])
            data = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"Warning: {file} is empty and will be skipped.")
        except pd.errors.ParserError:
            print(f"Error: {file} could not be parsed and will be skipped.")
        except Exception as e:
            print(f"Error: {file} could not be read due to {e} and will be skipped.")
        yield (filename, data)


def gen_cyphers(input_dir: str, output_dir) -> None:
    # Initialize the prompt and model
    prompt = UserPrompt()
    model = configure_llm()

    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    for filename, df in data:
        result = generate_cypher_queries(df, prompt, model)
        # Save the updated dataframe to a new CSV file
        result.to_csv(f"{output_dir}/{filename}", index=False)
        logger.info("Appended genearated queries to {}", filename)

    logger.info("Cypher generation complete.")
