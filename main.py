import os
from introspection import get_neo4j_metadata
from generate_prompt import SystemPrompt, UserPrompt
from ollama import chat
from ollama import ChatResponse
from drivers.dataloader import download_neo4j_text2cypher
import google.generativeai as genai
from pandas import DataFrame
from typing import Union
from time import sleep
from drivers.loadenv import load_env


def generate_cypher_queries(prompt: Union[UserPrompt, SystemPrompt]) -> dict:

    cypher_query_pairs = {}

    data = download_neo4j_text2cypher()
    print(data.head)
    
    # Build prompts to generate required Cypher queries
    for index, row in data.iterrows():

        nlp_query = row["question"]
        db_schema = row["schema"]
        ground_truth = row["cypher"]
        unique_id = row["instance_id"]

        user_prompt = prompt.create_prompt_builder().build_prompt(
        role="user",
        context=str(nlp_query),
        input_data=str(db_schema)
        )

        message_user = {
            "role": user_prompt['role'], 
            'content': {
                "Task": user_prompt['context'],
                "Instructions": "Use only the provided relationship types and properties. \
                    Do not use any other relationship types or properties that are not provided. \
                    Return just the cypher query inside three quotes and nothing else. \
                    If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.",
                "Schema": str(user_prompt['input_data'])
            }
        }

        response = model.generate_content(str(message_user))
        cypher_query_pairs.update(
            {
                "nlp_query": user_prompt["context"],
                "real": ground_truth,
                "generated": str(response.text).replace("\n", " ").replace("```cypher", " ")
            }
        )

        sleep(5)

        print(cypher_query_pairs)



if __name__ == "__main__":
    load_env()
    # Configure Gemini API
    genai.configure(api_key=os.getenv("GEMINI"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    generate_cypher_queries(UserPrompt())
