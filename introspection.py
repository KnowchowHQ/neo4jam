from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Update this to your database URI
username = "neo4j"
password = "your_password"

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    # Fetch Node Labels
    node_labels = session.run("CALL db.labels()").value()
    print("Node Labels:", node_labels)

    # Fetch Relationship Types
    relationship_types = session.run("CALL db.relationshipTypes()").value()
    print("Relationship Types:", relationship_types)

    # Fetch Schema Visualization
    schema = session.run("CALL db.schema.visualization()").data()
    print("Schema Visualization:", schema)

driver.close()
