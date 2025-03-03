from pathlib import Path
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher, sample_text2cypher
from ai.generator import process_file
from models import AVAILABLE_PROVIDERS
from pydantic import FilePath
from pathlib import Path

def download(to: str) -> None:
    download_neo4j_text2cypher(to)

def generate(source: FilePath, dest: Path, llm_api:AVAILABLE_PROVIDERS, model_name:str) -> None:
    process_file(source, dest, llm_api, model_name)

def preprocess(file: str, dest: str) -> None:
    preprocess_text2cypher(file, dest)

def sample(file: FilePath, dest: Path) -> None:
    sample_text2cypher(file, dest)


def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/.secrets/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download)
    app.command(help="Clean and split text2cypher data into subsets")(preprocess)
    app.command(help="Create subsets from preprocessed text2cypher data")(sample)
    app.command(help="Generate Cypher queries for a single text2cypher subset")(generate)
    app()


if __name__ == "__main__":
    run()
