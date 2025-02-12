from pathlib import Path
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher
from data.gencyphers import gen_cypher


def download(to: str) -> None:
    download_neo4j_text2cypher(to)


def preprocess(file: str, dest: str) -> None:
    preprocess_text2cypher(file, dest)

def generate_cypher(source:str, dest:str) -> None:
    gen_cypher(source, dest)


def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/confidential/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download)
    app.command(help="Preprocess text2cypher data")(preprocess)
    app.command(help="Generate Cypher queries for preprocessed data")(generate_cypher)
    app()


if __name__ == "__main__":
    run()