# Description: This file contains methods to evaluate the performance of the LLM.

from pathlib import Path
import pandas as pd
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame
from evaluation import metrics
from pydantic import DirectoryPath
from tqdm import tqdm


def evaluate_generated_cyphers(df: DataFrame) -> dict:
    try:
        tqdm.pandas(desc="Generate Cyphers")
        # Find the rouge scores
        rouge_metric = metrics.ROUGEMetric()
        try:
            df["QueryRougeScore"] = df.progress_apply(lambda x: rouge_metric.calculate(
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Rouge Score generated for {}", df["database_reference_alias"].unique())
        except IndexError as ie:
            logger.info(ie)

        # Find the BLEU scores
        bleu_metric = metrics.BLEUMetric()
        # metric = metrics.create_metric(bleu_metric_factory)
        try:
            df["QueryBLEUScore"] = df.progress_apply(lambda x: bleu_metric.calculate(
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Rouge Score generated for {}", df["database_reference_alias"].unique())
        except IndexError as ie:
            logger.info(ie)
        
        return df
    except KeyError as ke:
        logger.debug(ke)


# Method to load CSV files from a directory
def fetch_data_from_dir(directory: DirectoryPath) -> Generator[tuple[str, DataFrame], None, None]:
    """Fetches data from all CSV files in a directory and returns a DataFrame."""
    files = directory.glob("*.csv")
    for file in files:
        try:
            filename = file.name
            data = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"Warning: {file} is empty and will be skipped.")
        except pd.errors.ParserError:
            print(f"Error: {file} could not be parsed and will be skipped.")
        except Exception as e:
            print(f"Error: {file} could not be read due to {e} and will be skipped.")
        yield (filename, data)

def evaluate(input_dir: DirectoryPath, output_dir: DirectoryPath) -> None:
    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    for filename, df in data:
        result = evaluate_generated_cyphers(df)
        # Save the updated dataframe to a new CSV file
        result.to_csv(f"{output_dir}/{filename}", index=False)
        logger.info("Appended genearated queries to {}", filename)

    logger.info("Cypher generation complete.")