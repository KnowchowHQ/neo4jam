from pathlib import Path
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher


def download(to: str) -> None:
    download_neo4j_text2cypher(to)


def preprocess(file: str, dest: str) -> None:
    preprocess_text2cypher(file, dest)


def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/confidential/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download)
    app.command(help="Preprocess text2cypher data")(preprocess)
    app()


if __name__ == "__main__":
    run()