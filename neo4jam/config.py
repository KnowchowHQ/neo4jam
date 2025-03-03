import json
from pydantic import BaseModel, RootModel, Field
from pydantic.types import Annotated


class Experiments(BaseModel):
    seed:int = Annotated[int, Field(..., description="Seed for random number generation")]


class Config(BaseModel):
    experiments: Experiments



with open("./.config/config.json", "r") as f:
    config = Config(**json.load(f))


if __name__ == "__main__":
    print(config.model_dump_json(indent=2))