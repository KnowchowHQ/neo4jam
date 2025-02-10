from constants.globalconstant import *
import time
from loguru import logger
import pika
from pika.adapters.blocking_connection import BlockingChannel
import benchmark.evaluationmetrics as metrics
from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError

from drivers.csvhandler import CSVHandler


def connect_rabbitmq_server() -> tuple[BlockingChannel, BlockingChannel]:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    return (channel, connection)


def connect_neo4j_server(uri: str, auth=tuple[str, str]) -> GraphDatabase.driver:
    driver = GraphDatabase.driver(uri, auth=auth)
    driver.verify_connectivity()
    logger.debug("Connected to database {}", uri)
    return driver


def execute_cypher_query_pairs(index: str, query: tuple[str, str]) -> list:
    try:
        databases = DATABASE_REFERENCES.keys()
        referenced_db = CYPHER_QUERY_PAIRS[index]["database_reference"]
        logger.warning("Referenced DB: {}", referenced_db)
        logger.warning("Databases: {}", databases)
        
        if referenced_db is None:
            logger.info("No database reference present in the data!")
            return ["None", "None"]
        
        elif referenced_db in databases:
            db = referenced_db
            logger.debug("Accessing DB: {}", db)
            logger.debug("DB Info: {}", DATABASE_REFERENCES[db])

            driver = connect_neo4j_server(
                uri=DATABASE_REFERENCES[db]["uri"],
                auth=(DATABASE_REFERENCES[db]["username"],DATABASE_REFERENCES[db]["password"]),
            )
            try:
                result_real = driver.execute_query(query[0])
                result_generated = driver.execute_query(query[1])
                # logger.debug("Real: {}", result_real)
                # logger.debug("Generated: {}", result_generated)
                return [str(result_real), str(result_generated)]
            except CypherSyntaxError as cse:
                logger.error(cse)
                return [str(result_real), "None"]
        else:
            logger.info("No database reference for {} found!", referenced_db)
            return ["None", "None"]
    except KeyError as ke:
        logger.error(ke)
        return


def evaluate_generated_cyphers(ch, method, properties, body) -> None:
    try:
        logger.error(CONNECTION_INFO["result"])
        if body.decode() == CLOSE_MESSAGING:
            logger.warning("API quota reached. Closing the messaging service...")
            CONNECTION_INFO["subscriber"]["channel"].stop_consuming()
            return
             
        if len(CYPHER_QUERY_PAIRS) != 0:

            # Find the rouge scores
            rouge_metric_factory = metrics.ROUGEMetricFactory()

            try:

                score = metrics.evaluate_model(
                    factory=rouge_metric_factory,
                    predictions=[CYPHER_QUERY_PAIRS[body.decode()]["generated"]],
                    references=[CYPHER_QUERY_PAIRS[body.decode()]["real"]],
                )
                logger.info("Rouge Score: {}", score)
                CYPHER_QUERY_PAIRS[body.decode()]["QueryRougeScore"] = score
                # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
            except IndexError as ie:
                logger.info(ie)

            # Find the BLEU scores
            bleu_metric_factory = metrics.BLEUMetricFactory()

            try:
                score = metrics.evaluate_model(
                    factory=bleu_metric_factory,
                    predictions=[CYPHER_QUERY_PAIRS[body.decode()]["generated"]],
                    references=[CYPHER_QUERY_PAIRS[body.decode()]["real"]],
                )
                logger.info("BLEU score: {}", score)
                CYPHER_QUERY_PAIRS[body.decode()]["QueryBLEUScore"] = score
                # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
            except IndexError as ie:
                logger.info(ie)

            # Execute the cypher queries
            result_real, result_gen = execute_cypher_query_pairs(
                body.decode(),
                query=(
                    CYPHER_QUERY_PAIRS[body.decode()]["real"],
                    CYPHER_QUERY_PAIRS[body.decode()]["generated"],
                ),
            )
            # logger.info("Real: {}", result_real)
            # logger.info("Generated: {}", result_gen)

            # Find Rouge score for the cypher query execution result
            try:
                CYPHER_QUERY_PAIRS[body.decode()]["ExecRougeScore"] = (
                    metrics.evaluate_model(
                        factory=rouge_metric_factory,
                        predictions=[result_gen],
                        references=[result_real],
                    )
                )
                # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
            except KeyError as ke:
                logger.info(ke)

            # Find BLEU score for the cypher query execution result
            try:
                CYPHER_QUERY_PAIRS[body.decode()]["ExecBLEUScore"] = (
                    metrics.evaluate_model(
                        factory=bleu_metric_factory,
                        predictions=[result_gen],
                        references=[result_real],
                    )
                )
                # logger.info(CYPHER_QUERY_PAIRS[body.decode()])
            except KeyError as ke:
                logger.info(ke)

        else:
            logger.info("No data available for cypher evaluation!")
    except KeyError as ke:
        logger.info(CYPHER_QUERY_PAIRS)
    except Exception as e:
        logger.error(e)
        


def evaluation_execution_loop():
    # Open CSV file to read the generated cyphers
    csv_handler = CSVHandler(RESULT_FILE_PATH, INPUT_COLUMNS) 

    # channel, connection = connect_rabbitmq_server()
    # CONNECTION_INFO["subscriber"] = {"channel": channel, "connection": connection}

    # while True:
    #     try:
    #         channel.basic_consume(
    #             queue=MESSAGE_QUEUE_EVAL,
    #             auto_ack=True,
    #             on_message_callback=evaluate_generated_cyphers,
    #         )

    #         channel.start_consuming()

    #     except pika.exceptions.StreamLostError:
    #         print("Connection lost. Reconnecting...")
    #         time.sleep(5)  # Wait before retrying
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         break


if __name__ == "__main__":
    evaluation_execution_loop()
