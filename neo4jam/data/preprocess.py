from typing import Union
from config import config
from loguru import logger
import os
import pandas as pd
from pydantic import FilePath, DirectoryPath


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


def sample_text2cypher(
    path: Union[FilePath, DirectoryPath],
    dest: Union[FilePath, DirectoryPath],
) -> None:
    size = config.preprocessing.sample_sz
    if isinstance(size, int):
        sampling_params = {"n": size}
    elif isinstance(size, float):
        sampling_params = {"frac": size}
    else:
        raise ValueError("Sample size must be an integer or a float")

    if path.is_dir():
        paths = path.glob("*.csv")
    
    else:
        paths = [path]

    for path in paths:
        df = pd.read_csv(path)
        logger.info("Read data from {}", path)

        nrows= df.shape[0]

        if isinstance(size, int) and nrows < size:
            logger.warning("Data size is smaller than the sample size. Skipping sampling")
            sampled_df = df
        
        else:
            sampled_df = df.sample(**sampling_params, random_state=config.experiments.seed)

        # Save the data
        sampled_df.to_csv(dest / os.path.basename(path), index=False)
        logger.info("Saved sampled data to {}", dest)
    logger.info("Sampling complete")
