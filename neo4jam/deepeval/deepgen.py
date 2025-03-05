# Connect to remote Neo4j databases and execute Cypher queries.
import json
from multiprocessing import Pool
import os
from loguru import logger
from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError
import pandas as pd
from typing import Generator
from pandas import DataFrame, Series
from pydantic import DirectoryPath
from constants.globalconstant import DATABASE_REFERENCES
from tqdm import tqdm

def __connect_neo4j_server__(uri: str, auth: tuple[str, str]) -> object:
    """Connect to a Neo4j server and return a driver object."""
    try:
        driver = GraphDatabase.driver(uri, auth=auth)
        driver.verify_connectivity()
        return driver
    except Exception as e:
        logger.error(f"Error connecting to Neo4j server: {e}")

def __execute_cypher_query__(data: Series, driver: object, filename: str, output_dir: DirectoryPath, db_name: str) -> None:
    try:
        results, summary, keys = driver.execute_query(data)

        # Save the results to respective files
        
        filepath = output_dir / db_name 
        logger.info(f"Saving results to {filepath}")
        os.makedirs(filepath, exist_ok=True)
        
        with open(filepath / f"{filename}.json", "w") as f:
            json.dump(str(results), f, indent=4)
    except Neo4jError as cse:
        logger.error(cse)
    except DriverError as de:
        logger.error(de)

# Method to load CSV files from a directory
def fetch_data_from_dir(directory: DirectoryPath) -> Generator[tuple[str, DataFrame], None, None]:
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

def deepgen(input_dir: DirectoryPath, output_dir: DirectoryPath) -> None:
    # Load data from a directory
    data = fetch_data_from_dir(input_dir)
    
    with Pool(10) as pool:
        pool.starmap(__deepgen__, [(df, output_dir, filename) for filename, df in data])
        
    logger.info("Deep Generation complete.")

def __deepgen__(df: DataFrame, output_dir: DirectoryPath, filename: str) -> None:
    desc = "Deep Generation {}".format(filename)
    tqdm.pandas(desc=desc)
    try:
        databases = DATABASE_REFERENCES.keys()
        referenced_db = df["database_reference_alias"].unique()
        logger.warning("Referenced DB: {}", referenced_db)
        logger.warning("Databases: {}", databases)

        if referenced_db is None:
            logger.info("No database reference present in the data!")
            return ["None", "None"]
        
        for db in referenced_db:
            if db not in databases:
                logger.error("Database reference not found in the database references!")
            else:
                logger.debug("Accessing DB: {}", db)
                logger.debug("DB Info: {}", DATABASE_REFERENCES[db])


                driver = __connect_neo4j_server__(
                            uri=DATABASE_REFERENCES[db]["uri"],
                            auth=(DATABASE_REFERENCES[db]["username"],DATABASE_REFERENCES[db]["password"]),
                            )
    
        # Execute Cypher queries for original and generated Cyphers
        logger.debug("Executing Cypher queries for original Cyphers")
        dir_path = output_dir / "real"
        df.progress_apply(lambda x: __execute_cypher_query__(x["cypher"], driver, x["instance_id"], dir_path, referenced_db[0]), axis=1)

        dir_path = output_dir / "generated"
        logger.debug("Executing Cypher queries for generated Cyphers")
        df.progress_apply(lambda x: __execute_cypher_query__(x["generated"], driver, x["instance_id"], dir_path, referenced_db[0]), axis=1)
        
        logger.info("Deep Generation complete for {}", filename)

    except KeyError as ke:
        logger.info("Dataframe columns: {}", df.columns)
        logger.error(ke)