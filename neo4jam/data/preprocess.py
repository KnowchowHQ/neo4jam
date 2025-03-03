from config import config
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


def sample_text2cypher(file: str, dest: str, frac: float | None, n: int | None) -> None:
    if frac is None and n is None:
        raise ValueError("Either frac or n must be provided")
    if frac is not None and n is not None:
        raise ValueError("Only one of frac or n must be provided")

    df = pd.read_csv(file)
    logger.info("Read data from {}", file)

    # Sample data
    if n is not None:
        sampled_df = df.sample(n=n, random_state=config.experiments.seed)
    else:
        sampled_df = df.sample(frac=frac, random_state=config.experiments.seed)

    # Save the data
    sampled_df.to_csv(dest, index=False)
    logger.info("Saved sampled data to {}", dest)
    logger.info("Sampling complete")
