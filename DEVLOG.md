Dec 16, 2024
- Poetry was getting hung on poetry install. `poetry install -vvv` reveled poetry was struck trying to access te Linux keyring. Ran `poetry config keyring.enabled false`

Feb 3, 2025
- Consolidate all settings in a single JSON file 
- [Optional] Parse and validate the JSON with Pydantic
- Download module / or script to get HF Neo4J datasets
- Preprocess module / or script to split the dataset

Feb 10, 2025
- Break up code into DVC compatible "stages"

Feb 11, 2025
- Continue DVC migration
- Migrate to new google-genai package