import logging
import socket
import ssl
import random

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server, randomword


def handle_message(client, topic, message):
    print(f"{topic}: {message}")
    received_messages = client.user_data
    assert received_messages is not None
    assert received_messages.get(topic) is None
    received_messages[topic] = message


def test_subscribe_to_multiple_topics(mqtt_server):
    """
    client 1: connect, subscribe to multiple topics
    client 2: publish messages to a superset of topics subscribed by the first client;
              each topic receives one message
    Check that the first client received only the messages sent to the subscribed topics.
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    host = "localhost"
    port = mqtt_server.port

    received_messages = {}
    pool = socket
    mqtt_client_sub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
        recv_timeout=5,
        user_data=received_messages,
    )

    logger.info(f"Connecting to MQTT broker (subscriber)")
    mqtt_client_sub.connect(session_id="client_sub")

    num_topics = random.randrange(16, 64)
    topics = [randomword(random.randrange(10, 30)) for _ in range(num_topics)]
    for topic in topics:
        # add_topic_callback() makes sure that the callback will be called only for messages
        # received on the specified topic.
        mqtt_client_sub.add_topic_callback(topic, handle_message)
        logger.info(f"subscribing to {topic}")
        mqtt_client_sub.subscribe(topic)

    mqtt_client_pub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
    )

    logger.info(f"Connecting to MQTT broker (publisher)")
    mqtt_client_pub.connect(session_id="client_pub")
    sent_msgs = {}
    for topic in topics:
        logger.info(f"publishing message to topic {topic}")
        message = f"message to {topic}"
        sent_msgs[topic] = message
        mqtt_client_pub.publish(topic, message)

    # Publish messages to some topics not subscribed to by the mqtt_client_sub.
    for topic in ["foo", "bar"]:
        assert topic not in topics
        logger.info(f"publishing message to topic {topic}")
        message = f"message to {topic}"
        mqtt_client_pub.publish(topic, message)

    # Wait for the messages to arrive.
    mqtt_client_sub.loop(5)
    mqtt_client_sub.disconnect()
    mqtt_client_pub.disconnect()

    logger.debug(f"messages received: {len(received_messages)}")
    assert len(sent_msgs) == len(received_messages)
    assert sent_msgs == received_messages
