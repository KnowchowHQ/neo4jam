def system_prompt():
    return """You are an AI assistant helping a user to write a Cypher 
        query to retrieve data from a Neo4j database. The user has provided you
        with a natural language query. You need to generate a Cypher query that
        retrieves the data the user is asking for. Do not output anything other
        than the Cypher query."""


def user_prompt(schema: str, question: str):
    return f"""Following is the Neo4j database schema for the following schema and user query.
            Schema: {schema}
            User query: {question}"""
