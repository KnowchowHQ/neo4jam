from collections import deque
from enum import Enum
from time import sleep, time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
import os
from typing import List, Optional, Union

from loguru import logger

class GEMINI_AVAILABLE_MODELS(Enum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"


class GeminiAPI:
    def __init__(self, model_name: GEMINI_AVAILABLE_MODELS, system_prompt: str | None = None):
        if model_name not in GEMINI_AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} is not available. Choose from {[e.value for e in GEMINI_AVAILABLE_MODELS]}")
        api_keys = [os.environ.get("GEMINI_1"), os.environ.get("GEMINI_2"), os.environ.get("GEMINI_3")]
        self._key_manager = GeminiAPIKeyManager(api_keys, per_day_quota=1000, max_per_min_quota=15, cool_off_period=60)

        self._client = genai.Client(api_key=self._key_manager.get_key())
        self._model = model_name
        self._system_prompt = system_prompt

    def generate(self, query: Union[str, list]) -> str:
        if isinstance(query, str):
            query = [query]

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=query,
                config=types.GenerateContentConfig(
                    system_instruction=self._system_prompt or None
                ),
            )
            return response.text
        except ClientError as e:
            logger.warning("Google request quota reached. Waiting...")
            self._client.update_api_key(self._key_manager.get_key())
        finally:
            response = self._client.models.generate_content(
                model=self._model,
                contents=query,
                config=types.GenerateContentConfig(
                    system_instruction=self._system_prompt or None
                ),
            )
            return response.text



class GeminiAPIKeyManager:
    def __init__(self, keys, per_day_quota=500, max_per_min_quota=15, cool_off_period=60):
        self.keys = deque(keys)
        self.per_day_quota = per_day_quota
        self.max_per_min_quota = max_per_min_quota
        self.cool_off_period = cool_off_period
        self.usage_count = 0
        self.day_start_time = time.time()
        self.min_start_time = time.time()
        self.key_usage = {key: {'min': 0, 'day': 0, 'last_used': 0} for key in keys}

    def get_key(self):
        # Check if it's a new day
        if time.time() - self.day_start_time > 24 * 60 * 60:
            self.reset_daily_usage()

        # Check if it's a new minute
        if time.time() - self.min_start_time > 60:
            self.reset_minute_usage()

        # Rotate through keys
        current_key = self.keys.popleft()
        self.keys.append(current_key)

        # Check if the current key can be used
        if (self.key_usage[current_key]['min'] < self.max_per_min_quota and
            self.key_usage[current_key]['day'] < self.per_day_quota and
            time.time() - self.key_usage[current_key]['last_used'] >= self.cool_off_period):
            self.key_usage[current_key]['min'] += 1
            self.key_usage[current_key]['day'] += 1
            self.key_usage[current_key]['last_used'] = time.time()
            self.usage_count += 1
            return current_key
        else:
            # If the current key cannot be used, find another key
            for _ in range(len(self.keys)):
                current_key = self.keys.popleft()
                self.keys.append(current_key)
                if (self.key_usage[current_key]['min'] < self.max_per_min_quota and
                    self.key_usage[current_key]['day'] < self.per_day_quota and
                    time.time() - self.key_usage[current_key]['last_used'] >= self.cool_off_period):
                    self.key_usage[current_key]['min'] += 1
                    self.key_usage[current_key]['day'] += 1
                    self.key_usage[current_key]['last_used'] = time.time()
                    self.usage_count += 1
                    return current_key

            # If no key is available, wait until the next minute
            time.sleep(60 - (time.time() - self.min_start_time))
            return self.get_key()

    def reset_minute_usage(self):
        self.min_start_time = time.time()
        for key in self.keys:
            self.key_usage[key]['min'] = 0

    def reset_daily_usage(self):
        self.day_start_time = time.time()
        for key in self.keys:
            self.key_usage[key]['day'] = 0


if __name__ == '__main__':
    # Example usage
    keys = ['key1', 'key2', 'key3']
    manager = GeminiAPIKeyManager(keys, per_day_quota=500, max_per_min_quota=15, cool_off_period=60)

    for _ in range(100):
        print(manager.get_key())
