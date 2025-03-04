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
from multiprocessing import Pool


def _parse_response(resp: str) -> str:
    try:
        # Remove Markdown code block: ```cypher
        resp = resp.replace("```cypher", "")
        # Remove Markdown code block: ```
        resp = resp.replace("```", "")
        # Remove leading and trailing whitespaces
        resp = resp.strip()
        return resp
    except Exception as e:
        logger.error("Error parsing response: {}", e)
        return resp


def _generate_single(schema: str, question: str, llm_api) -> str:
    resp = llm_api.generate(user_prompt(schema, question))
    return _parse_response(resp)


def _generate_for_dataset(
    datafile: FilePath,
    dest: Path,
    llm_api,
) -> None:
    tqdm.pandas(desc="process file")
    df = pd.read_csv(datafile)
    df["generated"] = df.progress_apply(
        lambda x: _generate_single(x["schema"], x["question"], llm_api), axis=1
    )

    # Save the updated dataframe to a new CSV file
    filename = datafile.name
    df.to_csv(Path(dest, filename), index=False)

    logger.info("Writing genearated queries to {}", filename)


def generate_queries(
    dataset: Union[FilePath, DirectoryPath],
    dest: Path,
) -> None:
    llm_name = config.generation.provider
    model_name = config.generation.model
    llm_api_class = getattr(models, llm_name.value)
    llm_api = llm_api_class(
        model_name=model_name,
        system_prompt=system_prompt(),
    )

    if dataset.is_dir():
        paths = dataset.glob("*.csv")
    else:
        paths = [dataset]

    with Pool(16) as p:
        p.starmap(
            _generate_for_dataset, [(datafile, dest, llm_api) for datafile in paths]
        )

    logger.info("Cypher generation complete.")
