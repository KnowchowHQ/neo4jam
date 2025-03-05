from pathlib import Path
from typing import Union
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher, sample_text2cypher
from ai.generator import generate_queries
from models import AVAILABLE_PROVIDERS
from pydantic import FilePath, DirectoryPath
from pathlib import Path
from evaluation.evaluate import evaluate as evaluate_metrics
from evaluation.aggregate import aggregate_metrics
from deepeval.deepgen import deepgen


def download(to: str) -> None:
    download_neo4j_text2cypher(to)


def generate(source: Union[FilePath, DirectoryPath], dest: Path) -> None:
    generate_queries(source, dest)


def preprocess(file: str, dest: str) -> None:
    preprocess_text2cypher(file, dest)


def sample(file: Union[FilePath, DirectoryPath], dest: Path) -> None:
    sample_text2cypher(file, dest)


def evaluate(input_dir: DirectoryPath, output_dir: DirectoryPath) -> None:
    evaluate_metrics(input_dir, output_dir)

def aggregate(evals_dir: DirectoryPath) -> None:
    aggregate_metrics(evals_dir)

def deepgenerate(input_dir: DirectoryPath, output_dir: DirectoryPath) -> None:
    deepgen(input_dir, output_dir)

def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/.secrets/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download)
    app.command(help="Clean and split text2cypher data into subsets")(preprocess)
    app.command(help="Create subsets from preprocessed text2cypher data")(sample)
    app.command(help="Generate Cypher queries for a single text2cypher subset")(
        generate
    )
    app.command(help="Evaluate generated Cypher queries")(evaluate)
    app.command(help="Aggregate evaluation metrics")(aggregate)
    app.command(help="Generate Cypher queries using DeepGen")(deepgenerate)
    app()


if __name__ == "__main__":
    run()
