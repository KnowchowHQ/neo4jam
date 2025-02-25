from enum import Enum
from .google import GeminiAPI


class AVAILABLE_PROVIDERS(Enum):
    Google = "GeminiAPI"
    OpenAI = "OpenAI"
