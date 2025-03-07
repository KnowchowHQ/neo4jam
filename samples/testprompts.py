from neo4jam.data.generate_prompt import SystemPrompt, UserPrompt


# Generate the system prompt
prompt = SystemPrompt()

system_prompt = prompt.create_prompt_builder().build_prompt(
    role="system",
    context="You are a Neo4j database expert and you are familiar with Cypher commands"
)

print("Generated System Promt: {}".format(system_prompt))

ollama_message_system = { 
    "role": system_prompt['role'], 
    'content': system_prompt['context']
    }


# Generate the user prompt

prompt = UserPrompt()

user_prompt = prompt.create_prompt_builder().build_prompt(
    
    role="user",
    context="Generate a cypher query to retrieve list of all the movies in neo4j database. The following JSON corresponds to a neo4j schema.",
    input_data=get_neo4j_metadata(uri=uri, username=username, password=password)   
)

print("Generated User Prompt: {}".format(user_prompt))


ollama_message_user = { 
    "role": user_prompt['role'], 
    'content': user_prompt['context'] + "\n" + str(user_prompt['input_data'])
    }

# response = chat(model="qwen2.5-coder:14b", messages=[ollama_message_system])


response = model.generate_content(str(ollama_message_user))
print(response.text)



user_prompt = prompt.create_prompt_builder().build_prompt(
    
    role="user",
    context="Generate a cypher query to find the list of movies in which Tom Cruise and Meg Ryan both acted in. The following JSON corresponds to a neo4j schema.",
    input_data=get_neo4j_metadata(uri=uri, username=username, password=password)   
)

print("Generated User Prompt: {}".format(user_prompt))

ollama_message_user = { 
    "role": user_prompt['role'], 
    'content': user_prompt['context'] + "\n" + str(user_prompt['input_data'])
    }

response = model.generate_content(str(ollama_message_user))
print(response.text)



user_prompt = prompt.create_prompt_builder().build_prompt(
    
    role="user",
    context="Generate a cypher query to find all Persons born between 1980 and 1990. Return the name and date of birth in descending order. The following JSON corresponds to a neo4j schema.",
    input_data=get_neo4j_metadata(uri=uri, username=username, password=password)   
)

print("Generated User Prompt: {}".format(user_prompt))

ollama_message_user = { 
    "role": user_prompt['role'], 
    'content': user_prompt['context'] + "\n" + str(user_prompt['input_data'])
    }

response = model.generate_content(str(ollama_message_user))
print(response.text)