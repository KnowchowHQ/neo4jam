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

def generate_prompt(instruction=None, context=None, input_data=None, output_indicator=None):
    """
    Generates a structured prompt with components: instruction, context, input data, and output indicator.
    
    Args:
        instruction (str): The main task or goal for the system/user.
        context (str): Background information or additional details to aid in the task.
        input_data (str): The specific input data for the task.
        output_indicator (str): A description or example of the expected output format.

    Returns:
        dict: A dictionary containing the structured prompt components.
    """
    prompt = {
        "instruction": instruction if instruction else "Provide a clear instruction for the task.",
        "context": context if context else "Provide relevant background or context to help understand the task.",
        "input_data": input_data if input_data else "Specify the input data required to complete the task.",
        "output_indicator": output_indicator if output_indicator else "Describe the expected output or result."
    }
    return prompt
