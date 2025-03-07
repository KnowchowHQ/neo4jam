# Description: This file contains methods to evaluate the performance of the LLM.

import json
from multiprocessing import Pool
import os
from pathlib import Path
import pandas as pd
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame
from ..evaluation import metrics
from pydantic import DirectoryPath
from tqdm import tqdm
import multiprocessing


def evaluate_generated_cyphers(file_real: str, file_gen: str, rouge_metric, bleu_metric) -> dict:
    tqdm.pandas(desc="Evaluate execution results for Cyphers")        
    data_real = json.load(open(file_real))
    data_gen = json.load(open(file_gen))
    rougue_score = rouge_metric.calculate(predictions=[data_gen], references=[data_real])
    bleu_score = bleu_metric.calculate(predictions=[data_gen], references=[data_real])
    return {"rouge": rougue_score, "bleu": bleu_score}


def fetch_data_from_dir(
    base_dir: DirectoryPath,
) -> Generator[tuple[str, str], None, None]:
    # Search for all the files inside base_dir/real
    search_dir = Path(base_dir, "real")
    file_set = set()
    for root, _, files in os.walk(search_dir):
        for file in files:
            file_set.add(Path(root, file))
        logger.info("Found {} files in the {} directory", len(file_set), root)

    # Loop over all the in real directory and find the corresponding files in the generated directory
    for real_file in file_set:
        if os.path.isfile(real_file):
            filepath = Path(str(real_file).replace("real", "generated"))
            if filepath.exists():
                yield (real_file, filepath)
            else:
                logger.warning(f"Warning: {filepath} not found and will be skipped.")


def deepeval(input_dir: DirectoryPath, output_dir: DirectoryPath) -> None:
    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    rouge_metric = metrics.ROUGEMetric()
    bleu_metric = metrics.BLEUMetric()

    optimal_cores = max(1, multiprocessing.cpu_count() - 1)
    logger.info("Using {} cores for evaluation", optimal_cores)
    with Pool(optimal_cores) as pool:
        pool.starmap(
            __deepeval__,
            [
                (real, generated, output_dir, rouge_metric, bleu_metric)
                for real, generated in data
            ],
        )

    logger.info("Evaluation complete.")


def __deepeval__(
    real_file: str,
    gen_file: str,
    output_dir: DirectoryPath,
    rouge_metric,
    bleu_metric,
) -> None:
    result = evaluate_generated_cyphers(real_file, gen_file, rouge_metric, bleu_metric)
    
    # Save the updated dataframe to a new json file
    filename = Path(real_file).name

    directory = Path(output_dir, Path(real_file).parts[-2])

    # Save the result to respective files
    os.makedirs(directory, exist_ok=True)
    with open (f"{directory}/{filename}", "w") as f:
        json.dump(result, f, indent=4)
    
    logger.info("Appended scores to {}", f"{directory}/{filename}")


if __name__ == "__main__":
    deepeval(
        input_dir=Path("/home/devel/neo4jam/data/text2cypher/deepgen"),
        output_dir=Path("/home/devel/neo4jam/data/text2cypher/deepeval"),
   )
