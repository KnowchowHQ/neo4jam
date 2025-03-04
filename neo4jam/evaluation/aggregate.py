from config import config
import pandas as pd
from typing import Generator
from pandas import DataFrame
from pydantic import DirectoryPath
from evaluation import metrics


def _aggregate_metrics(df: DataFrame, rouge_metric, bleu_metric) -> tuple:

    rouge_agg_score = rouge_metric.calculate(
        predictions=df["generated"].tolist(), references=df["cypher"].tolist()
    )
    bleu_agg_score = bleu_metric.calculate(
        predictions=df["generated"].tolist(), references=df["cypher"].tolist()
    )
    return (rouge_agg_score, bleu_agg_score)


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
    rouge_metric = metrics.ROUGEMetric()
    bleu_metric = metrics.BLEUMetric()

    for filename, df in data:
        rouge_score, bleu_score = _aggregate_metrics(df, rouge_metric, bleu_metric)
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
