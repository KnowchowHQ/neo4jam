import importlib
import pandas as pd
import models
from models import AVAILABLE_PROVIDERS
from pydantic import FilePath
from pathlib import Path

def process_file(
    source: FilePath, dest: Path, llm_name: AVAILABLE_PROVIDERS, model_name: str
) -> None:
    df = pd.read_csv(source)
    llm_api_class = getattr(models, llm_name.value)
    
    llm_api = llm_api_class(
        model_name=model_name,
        system_prompt="""You are an AI assistant helping a user to write a Cypher 
        query to retrieve data from a Neo4j database. The user has provided you
        with a natural language query. You need to generate a Cypher query that
        retrieves the data the user is asking for.""",
    )

    df["cypher"] = df["text"].apply(lambda x: llm_api.generate(x))
    df.to_csv(dest, index=False)
