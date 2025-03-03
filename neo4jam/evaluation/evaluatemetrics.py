# Description: This file contains methods to evaluate the performance of the LLM.

import math
import os
from pathlib import Path
import sys
import pandas as pd
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame

# Add the directory containing generate_prompt.py to the Python path
parent_dir = Path(__file__).resolve().parents[2]
sys.path.append(os.path.join(parent_dir, "benchmark"))
sys.path.append(os.path.join(parent_dir, "constants"))

import metrics
from globalconstant import DATABASE_REFERENCES


def execute_cypher_query_pairs(index: str, query: tuple[str, str]) -> list:
    # try:
    #     databases = DATABASE_REFERENCES.keys()
    #     referenced_db = CYPHER_QUERY_PAIRS[index]["database_reference"]
    #     logger.warning("Referenced DB: {}", referenced_db)
    #     logger.warning("Databases: {}", databases)
        
    #     if referenced_db is None:
    #         logger.info("No database reference present in the data!")
    #         return ["None", "None"]
        
    #     elif referenced_db in databases:
    #         db = referenced_db
    #         logger.debug("Accessing DB: {}", db)
    #         logger.debug("DB Info: {}", DATABASE_REFERENCES[db])

    #         driver = connect_neo4j_server(
    #             uri=DATABASE_REFERENCES[db]["uri"],
    #             auth=(DATABASE_REFERENCES[db]["username"],DATABASE_REFERENCES[db]["password"]),
    #         )
    #         try:
    #             result_real = driver.execute_query(query[0])
    #             result_generated = driver.execute_query(query[1])
    #             # logger.debug("Real: {}", result_real)
    #             # logger.debug("Generated: {}", result_generated)
    #             return [str(result_real), str(result_generated)]
    #         except CypherSyntaxError as cse:
    #             logger.error(cse)
    #             return [str(result_real), "None"]
    #     else:
    #         logger.info("No database reference for {} found!", referenced_db)
    #         return ["None", "None"]
    # except KeyError as ke:
    #     logger.error(ke)
    #     return
    return {}

def evaluate_generated_cyphers(df: DataFrame) -> dict:
    try:
        # Find the rouge scores
        rouge_metric_factory = metrics.ROUGEMetricFactory()
        try:
            df["QueryRougeScore"] = df.apply(lambda x: metrics.evaluate_model(
                factory=rouge_metric_factory, 
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Rouge Score generated for {}", df["database_reference_alias"])
        except IndexError as ie:
            logger.info(ie)

        # Find the BLEU scores
        bleu_metric_factory = metrics.BLEUMetricFactory()
        try:
            df["QueryBLEUScore"] = df.apply(lambda x: metrics.evaluate_model(
                factory=bleu_metric_factory, 
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Rouge Score generated for {}", df["database_reference_alias"])
        except IndexError as ie:
            logger.info(ie)


        # Apply a function to the cypher column of dataframe
        # df["ExecRougeScore"], df["ExecBLEUScore"] = zip(
        #     *df["cypher"].apply(execute_cypher_query_pairs)
        # )
        return df
    except KeyError as ke:
        logger.debug(ke)

    #     # Execute the cypher queries
    #     result_real, result_gen = execute_cypher_query_pairs(
    #         body.decode(),
    #         query=(
    #             CYPHER_QUERY_PAIRS[body.decode()]["cypher"],
    #             CYPHER_QUERY_PAIRS[body.decode()]["generated"],
    #         ),
    #     )
    #         try:
    #             CYPHER_QUERY_PAIRS[body.decode()]["ExecRougeScore"] = (
    #                 metrics.evaluate_model(
    #                     factory=rouge_metric_factory,
    #                     predictions=[result_gen],
    #                     references=[result_real],
    #                 )
    #             )
    #             # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
    #         except KeyError as ke:
    #             logger.info(ke)

    #         # Find BLEU score for the cypher query execution result
    #         try:
    #             CYPHER_QUERY_PAIRS[body.decode()]["ExecBLEUScore"] = (
    #                 metrics.evaluate_model(
    #                     factory=bleu_metric_factory,
    #                     predictions=[result_gen],
    #                     references=[result_real],
    #                 )
    #             )
    #             # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
    #         except KeyError as ke:
    #             logger.info(ke)
    #     else:
    #         logger.info("No data available for cypher evaluation!")
    # except KeyError as ke:
    #     logger.info(CYPHER_QUERY_PAIRS)
    # except Exception as e:
    #     logger.error(e)


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

def cypher_evaluation(input_dir: str, output_dir) -> None:
    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    for filename, df in data:
        logger.debug("Processing file: {}", filename)
        result = evaluate_generated_cyphers(df)
        # Save the updated dataframe to a new CSV file
        result.to_csv(f"{output_dir}/{filename}", index=False)
        logger.info("Appended queries evaluation results to {}", filename)

    logger.info("Cypher output evaluation completed.")


if __name__ == "__main__":
    cypher_evaluation("/home/devel/neo4jam/data/text2cypher/gencyphers", "/home/devel/neo4jam/data/text2cypher/evaluated")