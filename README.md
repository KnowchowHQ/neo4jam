<h1 style="border-bottom: none;">Neo4jam</h1>  
<i>Experiments in AI-generated Neo4j Cypher queries</i>


---

## About
We investigate the effectiveness of using large language models to generate accurate Cypher queries from natural language queries. We use the HuggingFace [Text2Cypher][1] dataset which contains natural language and Cypher query pairs along with the schemas for 17 public Neo4j databases. 



[1]: https://huggingface.co/datasets/neo4j/text2cypher-2024v1


## Use

### Setup

- Install `pyenv` 
- Install an isolated Python interpreter with `pyenv install 3.12`
- Install `Poetry` 
- Clone this repo
- Step into the project directory `cd neo4jam`
- Activate the Python interpreter `pyenv local 3.12`
- Run `poetry install` to install all dependencies
- Edit DVC config file [.dvc/config] to set the URL for DVC remote, where DVC will store data

### Usage
- Run `dvc repro` to run all experiments
- OR `dvc repro -s <stage-name>` to run a specific DVC stage (check [dvc.yaml](dvc.yaml) for stage names)
- Run `dvc commit` and `dvc push` to save changes to the data


> Note: At the moment our DVC remote is private so you cannot `dvc pull` from our DVC repo and instead need to set up your own remote, run the experiments and upload the data to your remote
