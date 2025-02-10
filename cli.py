from typer import Typer
from data.download import download_neo4j_text2cypher


def run():
    app = Typer()
    app.command(help="Download text2cypher data from HuggingFace")(download_neo4j_text2cypher)
    app()


if __name__ == "__main__":
    run()