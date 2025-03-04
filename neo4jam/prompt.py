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
    Only output the cypher query and DO NOT include Markdown or any other formatting.      
    Schema: {schema}
    User Query: {question}
    Example: 
        Schema: 
            "Node properties:
            - **Question**
            - `favorites`: INTEGER Example: ""0""
            - `answered`: BOOLEAN 
            - `text`: STRING Example: ""### This is:  Bug    ### Specifications  OS: Win10""
            - `link`: STRING Example: ""https://stackoverflow.com/questions/62224586/playg""
            - `createdAt`: DATE_TIME Min: 2020-06-05T16:57:19Z, Max: 2020-06-05T21:49:16Z
            - `title`: STRING Example: ""Playground is not loading with apollo-server-lambd""
            - `id`: INTEGER Min: 62220505, Max: 62224586
            - `upVotes`: INTEGER Example: ""0""
            - `score`: INTEGER Example: ""-1""
            - `downVotes`: INTEGER Example: ""1""
            - **Tag**
            - `name`: STRING Example: ""aws-lambda""
            - **User**
            - `image`: STRING Example: ""https://lh3.googleusercontent.com/-NcFYSuXU0nk/AAA""
            - `link`: STRING Example: ""https://stackoverflow.com/users/10251021/alexandre""
            - `id`: INTEGER Min: 751, Max: 13681006
            - `reputation`: INTEGER Min: 1, Max: 420137
            - `display_name`: STRING Example: ""Alexandre Le""
            Relationship properties:

            The relationships:
            (:Question)-[:TAGGED]->(:Tag)
            (:User)-[:ASKED]->(:Question)"
        User Query:
            List the top 5 users who have interacted with 'louisgray.com'.
        Expected Output:
            MATCH (u:User)-[:ASKED]->(q:Question) WITH u, COUNT(q) AS question_count ORDER BY question_count DESC LIMIT 5 RETURN u.display_name AS user, question_count
        """
