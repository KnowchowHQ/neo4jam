def system_prompt():
    return """You are an AI assistant helping a user to write a Cypher 
        query to retrieve data from a Neo4j database. The user has provided you
        with a natural language query. You need to generate a Cypher query that
        retrieves the data the user is asking for. Do not output anything other
        than the Cypher query, including any markdown or other formatting."""


def user_prompt(schema: str, question: str):
    if not schema:
        raise ValueError("Schema cannot be empty.")
    if not question:
        raise ValueError("Question cannot be empty.")
    return f"""Following is the Neo4j database schema for the following schema and user query.
            Schema: {schema}
            User query: {question}"""
