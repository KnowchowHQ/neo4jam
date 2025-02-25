import os
import pandas as pd
from pandas import DataFrame
from huggingface_hub import login
from loguru import logger

def login_huggingface_hub():
    login(token=os.getenv("HUGGING_FACE"))


def download_neo4j_text2cypher(to: str) -> None:
    """
    The Neo4j-Text2Cypher (2024) Dataset brings together instances from publicly available datasets, 
    cleaning and organizing them for smoother use. 

    Each entry includes a “question, schema, cypher” triplet at minimum, with a total of 44,387 instances — 
    39,554 for training and 4,833 for testing.

    ---------------------------------------------------------------------------------------------------------------------
    | Field                      |                Description                                                           |  
    ---------------------------------------------------------------------------------------------------------------------
    | “question” 	             |   Users’ textual question. E.g., “What is the total number of companies?”            |
    ---------------------------------------------------------------------------------------------------------------------          
    | “schema”	                 |   The database schema.                                                               |
    ---------------------------------------------------------------------------------------------------------------------
    | “cypher”	                 |   Output cypher query. E.g., “MATCH (c:Company) RETURN COUNT(c)”                     |
    ---------------------------------------------------------------------------------------------------------------------
    | “data_source”	             |   Alias of the dataset source. E.g., "neo4jLabs_synthetic_gpt4turbo"                 |
    ---------------------------------------------------------------------------------------------------------------------
    | “database_reference_alias” |	 Alias of the database (if available). E.g., None, "neo4jlabs_demo_db_stackoverflow"|
    ---------------------------------------------------------------------------------------------------------------------
    | “instance_id”	             |   Incremental index assigned per row.                                                |
    ---------------------------------------------------------------------------------------------------------------------

    """
    try:
        logger.info("Trying to login into Huggingface...")
        login_huggingface_hub()
        logger.info("Loggedin successfully.")

    except ValueError:
        logger.info("Could not login into Huggingface. Try checking if the supplied token is valid.")
        raise ValueError()
    
    splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
    df = pd.read_parquet("hf://datasets/neo4j/text2cypher-2024v1/" + splits["train"])

    # Log details about df
    logger.info("Downloaded data from huggingface.")
    logger.info("DF summary: {}", df.info())

    # Save the data to the specified location
    df.to_csv(to, index=False)
    logger.info("Saved data to {}", to)