import logging
import socket
import ssl
import random
import string

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from . import FakeConnectionManager

from ..common import mqtt_server

RECEIVED_MESSAGES = {}


def handle_message(client, topic, message):
    print(f"{client}# {topic}: {message}")
    # Once MiniMQTT has on_message with user_data, switch to that.
    global RECEIVED_MESSAGES
    RECEIVED_MESSAGES[topic] = message


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def test_subscribe_to_multiple_topics(mqtt_server):
    """
    client 1: connect, subscribe to multiple topics
    client 2: publish messages to a superset of topics subscribed by the first client
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    host = "localhost"
    port = mqtt_server.port

    pool = socket
    mqtt_client_sub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
        recv_timeout=5,
    )

    mqtt_client_sub._connection_manager = FakeConnectionManager(pool)

    logger.info(f"Connecting to MQTT broker (subscriber)")
    mqtt_client_sub.connect()

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

    mqtt_client_pub._connection_manager = FakeConnectionManager(pool)

    logger.info(f"Connecting to MQTT broker (publisher)")
    mqtt_client_pub.connect()
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

    logger.debug(f"messages received: {len(RECEIVED_MESSAGES)}")
    assert len(sent_msgs) == len(RECEIVED_MESSAGES)
    assert sent_msgs == RECEIVED_MESSAGES
