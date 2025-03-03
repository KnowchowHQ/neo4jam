def system_prompt():
    return """You are an AI assistant helping a user to write a Cypher 
        query to retrieve data from a Neo4j database. The user has provided you
        with a natural language query. You need to generate a Cypher query that
        retrieves the data the user is asking for."""


def user_prompt(schema: str, question: str):
    if not schema:
        raise ValueError("Schema cannot be empty.")
    if not question:
        raise ValueError("Question cannot be empty.")
    return f"""Generate cypher query for the following schema and user query.
    Only output the cypher query as a string without any formatting.      
    Schema: {schema}
    User query: {question}"""
