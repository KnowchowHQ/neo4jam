from collections import deque
from enum import Enum
from time import sleep, time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
import os
from typing import List, Optional, Union
import functools
from loguru import logger


class GEMINI_AVAILABLE_MODELS(Enum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"


from time import sleep, time
from loguru import logger


class RateLimit:
    def __init__(self, max_per_min, cool_off_period):
        self.max_per_min = max_per_min
        self.cool_off_period = cool_off_period
        self.window_start = None
        self.nb_calls = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(obj, *args, **kwargs):
            if self.window_start is None or time() - self.window_start > 60:
                self.window_start = time()
                self.nb_calls = 0

            if self.nb_calls >= self.max_per_min:
                sleep_time = self.cool_off_period - (time() - self.window_start)
                if sleep_time > 0:
                    logger.info(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
                    sleep(sleep_time)
                self.window_start = time()
                self.nb_calls = 0

            self.nb_calls += 1
            return func(obj, *args, **kwargs)

        return wrapper



class GeminiAPI:
    def __init__(
        self, model_name: GEMINI_AVAILABLE_MODELS, system_prompt: str | None = None
    ):
        if model_name not in GEMINI_AVAILABLE_MODELS:
            raise ValueError(
                f"Model {model_name} is not available. Choose from {[e.value for e in GEMINI_AVAILABLE_MODELS]}"
            )

        self._client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self._model = model_name
        self._system_prompt = system_prompt

    @RateLimit(max_per_min=100, cool_off_period=60)
    def generate(self, query: Union[str, list]) -> str:
        if isinstance(query, str):
            query = [query]

        response = self._client.models.generate_content(
            model=self._model,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt or None
            ),
        )
        return response.text
