from pathlib import Path
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher
from ai.generator import process_file

def download(to: str) -> None:
    download_neo4j_text2cypher(to)


def preprocess(file: str, dest: str) -> None:
    preprocess_text2cypher(file, dest)


def generate(source: str, dest: str) -> None:
    process_file(source, dest)


def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/.secrets/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download)
    app.command(help="Clean and split text2cypher data into subsets")(preprocess)
    app.command(help="Generate Cypher queries for a single text2cypher subset")(generate)
    app()


if __name__ == "__main__":
    run()
