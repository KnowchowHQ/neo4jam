from neo4j import GraphDatabase


def get_neo4j_metadata(uri: str, username: str, password: str) -> dict:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    metadata = {}

    with driver.session() as session:
        # Fetch Node Labels
        node_labels = session.run("CALL db.labels()").value()
        metadata['node_labels'] = node_labels
        
        # Fetch Relationship Types
        relationship_types = session.run("CALL db.relationshipTypes()").value()
        metadata['relationship_types'] = relationship_types

        # Fetch Schema Visualization
        schema = session.run("CALL db.schema.visualization()").data()
        metadata['schema'] = schema

    driver.close()
    return metadata