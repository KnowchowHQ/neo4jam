from loguru import logger
import pandas as pd
import models
from models import AVAILABLE_PROVIDERS
from pydantic import FilePath
from pathlib import Path
from prompt import system_prompt, user_prompt
from tqdm import tqdm


def process_file(
    source: FilePath, dest: Path, llm_name: AVAILABLE_PROVIDERS, model_name: str
) -> None:
    tqdm.pandas(desc="process file") # https://github.com/tqdm/tqdm?tab=readme-ov-file#pandas-integration

    df = pd.read_csv(source)
    llm_api_class = getattr(models, llm_name.value)

    llm_api = llm_api_class(
        model_name=model_name,
        system_prompt=system_prompt(),
    )
    # Fetch DB schema
    df["cypher"] = df.progress_apply(
        lambda x: llm_api.generate(user_prompt(x["schema"], x["question"])), axis=1
    )

    # Save the updated dataframe to a new CSV file
    if not dest.exists():
        dest.mkdir(parents=True)
    filename = source.name
    df.to_csv(f"{dest}/{filename}", index=False)

    logger.info("Appended genearated queries to {}", filename)
    logger.info("Cypher generation complete.")
