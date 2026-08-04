"""
Kafka/Redpanda stream consumer.

Consumes security events from streaming topics.
"""


from kafka import KafkaConsumer
import json



def create_consumer(
        topic,
        bootstrap_server="localhost:9092"
):

    consumer = KafkaConsumer(

        topic,

        bootstrap_servers=[
            bootstrap_server
        ],

        value_deserializer=lambda x:
            json.loads(
                x.decode("utf-8")
            ),

        auto_offset_reset="earliest"

    )

    return consumer



def consume_events(topic):

    consumer = create_consumer(
        topic
    )


    print(
        f"Listening on topic: {topic}"
    )


    for message in consumer:

        event = message.value

        process_event(
            event
        )



def process_event(event):

    print(
        "Received event:"
    )

    print(event)