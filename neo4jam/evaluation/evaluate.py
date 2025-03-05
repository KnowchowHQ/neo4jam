# Description: This file contains methods to evaluate the performance of the LLM.

from multiprocessing import Pool
from pathlib import Path
import pandas as pd
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame
from evaluation import metrics
from pydantic import DirectoryPath
from tqdm import tqdm


def evaluate_generated_cyphers(df: DataFrame, rouge_metric, bleu_metric) -> dict:
    try:
        tqdm.pandas(desc="Evaluate Generated Cyphers")
        try:
            df["QueryRougeScore"] = df.progress_apply(lambda x: rouge_metric.calculate(
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Rouge Score generated for {}", df["database_reference_alias"].unique())
        except IndexError as ie:
            logger.info(ie)

        # Find the BLEU scores
        try:
            df["QueryBLEUScore"] = df.progress_apply(lambda x: bleu_metric.calculate(
                predictions=[x["generated"]  if pd.notnull(x["generated"]) else " "], 
                references=[ x["cypher"]]), axis=1)
            
            logger.info("Bleu Score generated for {}", df["database_reference_alias"].unique())
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
    rouge_metric = metrics.ROUGEMetric()
    bleu_metric = metrics.BLEUMetric()

    with Pool(10) as pool:
        pool.starmap(__evaluate__, [(df, output_dir, filename, rouge_metric, bleu_metric) for filename, df in data])
       
    logger.info("Evaluation complete.")

def __evaluate__(df: DataFrame, output_dir: DirectoryPath, filename: str, rouge_metric, bleu_metric) -> None:
    result = evaluate_generated_cyphers(df, rouge_metric, bleu_metric)
    # Save the updated dataframe to a new CSV file
    result.to_csv(f"{output_dir}/{filename}", index=False)
    logger.info("Appended genearated scores to {}", filename)