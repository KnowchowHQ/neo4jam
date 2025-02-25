import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path

def load_env():
    load_dotenv(Path("./.secrets/.env"))
    print(os.getenv("GEMINI"))
    print(os.getenv("HUGGING_FACE"))