# Description: This file contains methods to evaluate the performance of the LLM.

from pathlib import Path
from turtle import pd
from typing import Generator, Union
from loguru import logger
from pandas import DataFrame

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

def evaluation_execution_loop(input_dir: str, output_dir) -> None:
    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    for filename, df in data:
        result = (df, prompt, model)
        # Save the updated dataframe to a new CSV file
        result.to_csv(f"{output_dir}/{filename}", index=False)
        logger.info("Appended genearated queries to {}", filename)

    logger.info("Cypher generation complete.")