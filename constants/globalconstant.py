CYPHER_QUERY_PAIRS = {}
GOOGLE_REQUEST_QUOTA = 1000
GOOGLE_PER_MIN_QUOTA = 15
MESSAGE_QUEUE_EVAL = "evaluate"
CLOSE_MESSAGING = "close"
CONNECTION_INFO = {}

# Local Neo4j credentials
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "Oakridge+100"

# List of Neo4j DBs used for evaluation [Refer: https://bratanic-tomaz.medium.com/crowdsourcing-text2cypher-dataset-e65ba51916d4]
# Information about the data and databases used for analysis [Refer: https://huggingface.co/datasets/neo4j/text2cypher-2024v1]

NEO4J_MOVIES_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_MOVIES_USERNAME = "movies"
NEO4J_MOVIES_PASSWORD = "movies"

NEO4J_FINCEN_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_FINCEN_USERNAME = "fincen"
NEO4J_FINCEN_PASSWORD = "fincen"

NEO4J_COMPANIES_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_COMPANIES_USERNAME = "companies"
NEO4J_COMPANIES_PASSWORD = "companies"

NEO4J_NETWORK_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_NETWORK_USERNAME = "network"
NEO4J_NETWORK_PASSWORD = "network"

NEO4J_TWITCH_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_TWITCH_USERNAME = "twitch"
NEO4J_TWITCH_PASSWORD = "twitch"

NEO4J_STACKOVERFLOW2_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_STACKOVERFLOW2_USERNAME = "stackoverflow2"
NEO4J_STACKOVERFLOW2_PASSWORD = "stackoverflow2"

NEO4J_RECOMMENDATIONS_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_RECOMMENDATIONS_USERNAME = "recommendations"
NEO4J_RECOMMENDATIONS_PASSWORD = "recommendations"

NEO4j_GAMEOFTHRONES_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4j_GAMEOFTHRONES_USERNAME = "gameofthrones"
NEO4j_GAMEOFTHRONES_PASSWORD = "gameofthrones"

NEO4J_GRANDSTACK_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_GRANDSTACK_USERNAME = "grandstack"
NEO4J_GRANDSTACK_PASSWORD = "grandstack"

NEO4J_TWITTER_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_TWITTER_USERNAME = "twitter"
NEO4J_TWITTER_PASSWORD = "twitter"

NEO4J_BUZZOVERFLOW_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_BUZZOVERFLOW_USERNAME = "buzzoverflow"
NEO4J_BUZZOVERFLOW_PASSWORD = "buzzoverflow"

NEO4J_NEOFLIX_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_NEOFLIX_USERNAME = "neoflix"
NEO4J_NEOFLIX_PASSWORD = "neoflix"

NEO4J_OFFSHORELEAKS_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_OFFSHORELEAKS_USERNAME = "offshoreleaks"
NEO4J_OFFSHORELEAKS_PASSWORD = "offshoreleaks"

NEO4J_NORTHWIND_URI = "neo4j+s://demo.neo4jlabs.com:7687/"
NEO4J_NORTHWIND_USERNAME = "northwind"
NEO4J_NORTHWIND_PASSWORD = "northwind"


DATABASE_REFERENCES = {
    "neo4jlabs_demo_db_fincen": {
        "uri": NEO4J_FINCEN_URI,
        "username": NEO4J_FINCEN_USERNAME,
        "password": NEO4J_FINCEN_PASSWORD,
    },
    "neo4jlabs_demo_db_movies": {
        "uri": NEO4J_MOVIES_URI,
        "username": NEO4J_MOVIES_USERNAME,
        "password": NEO4J_MOVIES_PASSWORD,
    },
    "neo4jlabs_demo_db_network": {
        "uri": NEO4J_NETWORK_URI,
        "username": NEO4J_NETWORK_USERNAME,
        "password": NEO4J_NETWORK_PASSWORD,
    },
    "neo4jlabs_demo_db_companies": {
        "uri": NEO4J_COMPANIES_URI,
        "username": NEO4J_COMPANIES_USERNAME,
        "password": NEO4J_COMPANIES_PASSWORD,
    },
    "neo4jlabs_demo_db_stackoverflow2": {
        "uri": NEO4J_STACKOVERFLOW2_URI,
        "username": NEO4J_STACKOVERFLOW2_USERNAME,
        "password": NEO4J_STACKOVERFLOW2_PASSWORD,
    },
    "neo4jlabs_demo_db_recommendations": {
        "uri": NEO4J_RECOMMENDATIONS_URI,
        "username": NEO4J_RECOMMENDATIONS_USERNAME,
        "password": NEO4J_RECOMMENDATIONS_PASSWORD,
    },
    "neo4jlabs_demo_db_gameofthrones": {
        "uri": NEO4j_GAMEOFTHRONES_URI,
        "username": NEO4j_GAMEOFTHRONES_USERNAME,
        "password": NEO4j_GAMEOFTHRONES_PASSWORD,
    },
    "neo4jlabs_demo_db_grandstack": {
        "uri": NEO4J_GRANDSTACK_URI,
        "username": NEO4J_GRANDSTACK_USERNAME,
        "password": NEO4J_GRANDSTACK_PASSWORD,
    },
    "neo4jlabs_demo_db_twitter": {
        "uri": NEO4J_TWITTER_URI,
        "username": NEO4J_TWITTER_USERNAME,
        "password": NEO4J_TWITTER_PASSWORD,
    },
    "neo4jlabs_demo_db_buzzoverflow": {
        "uri": NEO4J_BUZZOVERFLOW_URI,
        "username": NEO4J_BUZZOVERFLOW_USERNAME,
        "password": NEO4J_BUZZOVERFLOW_PASSWORD,
    },
    "neo4jlabs_demo_db_eoflix": {
        "uri": NEO4J_NEOFLIX_URI,
        "username": NEO4J_NEOFLIX_USERNAME,
        "password": NEO4J_NEOFLIX_PASSWORD,
    },
    "neo4jlabs_demo_db_offshoreleaks": {
        "uri": NEO4J_OFFSHORELEAKS_URI,
        "username": NEO4J_OFFSHORELEAKS_USERNAME,
        "password": NEO4J_OFFSHORELEAKS_PASSWORD,
    },
    "neo4jlabs_demo_db_northwind": {
        "uri": NEO4J_NORTHWIND_URI,
        "username": NEO4J_NORTHWIND_USERNAME,
        "password": NEO4J_NORTHWIND_PASSWORD,
    },
}
