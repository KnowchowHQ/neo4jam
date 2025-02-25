from google import genai
from google.genai import types
import os


class GeminiAPI:
    def __init__(self, model: str, system_prompt: str | None = None):
        self._client = genai.Client(api_key=os.environ.get("GEMINI"))
        self._model = model
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
