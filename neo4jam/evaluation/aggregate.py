from config import config
import pandas as pd
from typing import Generator
from pandas import DataFrame
from pydantic import DirectoryPath


# Method to load CSV files from a directory
def fetch_data_from_dir(
    directory: DirectoryPath,
) -> Generator[tuple[str, DataFrame], None, None]:
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


def aggregate_metrics(input_dir: DirectoryPath) -> None:
    data = fetch_data_from_dir(input_dir)
    scores = []
    for filename, df in data:
        rouge_score = df["QueryRougeScore"].mean()
        bleu_score = df["QueryBLEUScore"].mean()
        scores.append(
            {
                "filename": filename,
                "rouge_score": rouge_score,
                "bleu_score": bleu_score,
            }
        )
    scores_df = pd.DataFrame(
        data=scores, columns=["filename", "rouge_score", "bleu_score"]
    )
    scores_df.to_json(config.evaluation.report, orient="records", lines=True)
