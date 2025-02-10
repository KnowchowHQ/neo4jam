from loguru import logger
import os
import pandas as pd


def preprocess_text2cypher(file: str, dest: str) -> None:
    df = pd.read_csv(file)
    logger.info("Read data from {}", file)
    logger.info("DF summary: {}", df.info())

    # Drop rows with missing DB name
    df.dropna(subset=["database_reference_alias"], inplace=True)
    logger.info("Dropped rows with missing DB name")

    # Save the data, one CSV per DB
    if not os.path.exists(dest):
        os.makedirs(dest)
    for db in df["database_reference_alias"].unique():
        db_df = df[df["database_reference_alias"] == db]
        db_df.to_csv(f"{dest}/{db}.csv", index=False)
        logger.info("Saved data for {}", db)
    logger.info("Preprocessing complete")
