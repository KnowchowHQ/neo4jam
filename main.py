from introspection import get_neo4j_metadata


uri = "bolt://localhost:7687"  # Update this to your database URI
username = "neo4j"
password = "your_password"

print(get_neo4j_metadata(uri, username, password))