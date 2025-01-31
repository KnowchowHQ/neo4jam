from constants.globalconstant import *
from loguru import logger
import pika
from pika.adapters.blocking_connection import BlockingChannel
import benchmark.evaluationmetrics as metrics


def connect_rabbitmq_server() -> tuple[BlockingChannel, BlockingChannel]:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    return (channel, connection)



def evaluate_generated_cyphers(ch, method, properties, body) -> None:
    try:
        if body.decode() == CLOSE_MESSAGING:
            CONNECTION_INFO["subscriber"]["channel"].stop_consuming()
            CONNECTION_INFO["subscriber"]["connection"].close()
            return
        if len(CYPHER_QUERY_PAIRS) != 0:
            # Find the rouge scores
            rouge_metric_factory = metrics.ROUGEMetricFactory()

            try:

                score =metrics.evaluate_model(factory=rouge_metric_factory, 
                                              predictions=[CYPHER_QUERY_PAIRS[body.decode()]['generated']], 
                                              references=[CYPHER_QUERY_PAIRS[body.decode()]['real']])
                logger.info(score)
                CYPHER_QUERY_PAIRS[body.decode()]['score'] = score
                logger.info(CYPHER_QUERY_PAIRS[body.decode()])
            except IndexError as ie:
                logger.info(ie)
                return
        else:
            logger.info("No data available for cypher evaluation!")
    except KeyError as ke:
        logger.info(CYPHER_QUERY_PAIRS)


def evaluation_execution_loop():
    channel, connection = connect_rabbitmq_server()
    CONNECTION_INFO["subscriber"] = {"channel": channel, "connection": connection}
    channel.basic_consume(queue=MESSAGE_QUEUE_EVAL, 
                          auto_ack=True, 
                          on_message_callback=evaluate_generated_cyphers)
    channel.start_consuming()


if __name__ == "__main__":
    evaluation_execution_loop()