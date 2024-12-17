from introspection import get_neo4j_metadata
from generate_prompt import SystemPrompt, UserPrompt
from ollama import chat
from ollama import ChatResponse
from drivers.dataloader import download_neo4j_text2cypher
import google.generativeai as genai
from pandas import DataFrame
from typing import Union
from time import sleep


uri = "bolt://localhost:7687"  # Update this to your database URI
username = "neo4j"
password = "Oakridge+100"

# Configure Gemini API
genai.configure(api_key="AIzaSyD4MfUK8o7LKvI6PqOqu8XLrtkp4PDtrXs")
model = genai.GenerativeModel("gemini-1.5-flash")


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
            'content': user_prompt['context'] + "\n" + str(user_prompt['input_data'])
            }

        response = model.generate_content(str(message_user))
        cypher_query_pairs.update(
            {
            "real": ground_truth,
            "generated": response.text
            }
        )

        sleep(5)

        print(cypher_query_pairs)

generate_cypher_queries(UserPrompt())
