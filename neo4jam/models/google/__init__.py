from enum import Enum
from google import genai
from google.genai import types
import os


class GEMINI_AVAILABLE_MODELS(Enum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"


class GeminiAPI:
    def __init__(self, model_name: GEMINI_AVAILABLE_MODELS, system_prompt: str | None = None):
        if model_name not in GEMINI_AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} is not available. Choose from {[e.value for e in GEMINI_AVAILABLE_MODELS]}")
        self._client = genai.Client(api_key=os.environ.get("GEMINI"))
        self._model = model_name
        self._system_prompt = system_prompt

    def generate(self, query: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=[query],
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt or None
            ),
        )
        return response.text
