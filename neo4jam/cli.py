from pathlib import Path
from typer import Typer
from data.download import download_neo4j_text2cypher
from dotenv import load_dotenv
from data.preprocess import preprocess_text2cypher


def run():
    app = Typer()
    load_dotenv(Path("/home/devel/neo4jam/confidential/.env"))
    app.command(help="Download text2cypher data from HuggingFace")(download_neo4j_text2cypher)
    app.command(help="Preprocess text2cypher data")(preprocess_text2cypher)
    app()


if __name__ == "__main__":
    run()