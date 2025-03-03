import json
from pydantic import BaseModel, RootModel, Field
from pydantic.types import Annotated
from typing import Union


class Experiments(BaseModel):
    seed: int = Annotated[
        int, Field(..., description="Seed for random number generation")
    ]


class Preprocessing(BaseModel):
    sample_sz: Union[int, float] = Annotated[
        Union[int, float],
        Field(
            ...,
            description="Sample size for sampling the dataset. Can be a fraction or an integer set ",
        ),
    ]


class Config(BaseModel):
    experiments: Experiments
    preprocessing: Preprocessing


with open("./.config/config.json", "r") as f:
    config = Config(**json.load(f))


if __name__ == "__main__":
    print(config.model_dump_json(indent=2))
