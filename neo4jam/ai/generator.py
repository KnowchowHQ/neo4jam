from typing import Union
from loguru import logger
import pandas as pd
import models
from models import AVAILABLE_PROVIDERS
from pydantic import DirectoryPath, FilePath
from pathlib import Path
from prompt import system_prompt, user_prompt
from tqdm import tqdm
from config import config


def process_file(
    source: Union[FilePath, DirectoryPath],
    dest: Path,
) -> None:
    tqdm.pandas(    
        desc="process file"
    )
    llm_name = config.generation.provider
    model_name = config.generation.model
    llm_api_class = getattr(models, llm_name.value)
    llm_api = llm_api_class(
        model_name=model_name,
        system_prompt=system_prompt(),
    )

    if source.is_dir():
        paths = source.glob("*.csv")
    else:
        paths = [source]
    
    for path in paths:
      # https://github.com/tqdm/tqdm?tab=readme-ov-file#pandas-integration

        df = pd.read_csv(path)
            
        # Fetch DB schema
        df["generated"] = df.progress_apply(
            lambda x: llm_api.generate(user_prompt(x["schema"], x["question"])), axis=1
        )

        # Save the updated dataframe to a new CSV file
        filename = path.name
        df.to_csv(Path(dest, filename), index=False)

        logger.info("Appended genearated queries to {}", filename)
    logger.info("Cypher generation complete.")
