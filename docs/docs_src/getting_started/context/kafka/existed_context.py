from faststream import Context, FastStream
from faststream.kafka import KafkaBroker
from faststream.kafka.annotations import (
    ContextRepo,
    KafkaMessage,
    Logger,
    KafkaBroker as BrokerAnnotation,
)

broker_object = KafkaBroker("localhost:9092")
app = FastStream(broker_object)

@broker_object.subscriber("test-topic")
async def handle(
    logger=Context(),
    message=Context(),
    broker=Context(),
    context=Context(),
):
    logger.info(message)
    await broker.publish("test", "response")

@broker_object.subscriber("response-topic")
async def handle_response(
    logger: Logger,
    message: KafkaMessage,
    context: ContextRepo,
    broker: BrokerAnnotation,
):
    logger.info(message)
    await broker.publish("test", "response")
