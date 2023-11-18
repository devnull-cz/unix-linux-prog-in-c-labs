import logging
import socket
import ssl
import time
import random

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server

RECEIVED_MESSAGES = []

def handle_message(client, topic, message):
    print(f"{client}# {topic}: {message}")
    # Once MiniMQTT has on_message with user_data, switch to that.
    global RECEIVED_MESSAGES
    RECEIVED_MESSAGES.append(message)


def test_publish_by_many_to_single(mqtt_server):
    """
    client 1: connect, subscribe to single topic
    clients 2..n: connect, publish message to the topic, disconnect

    Once the messages are sent, the first client waits a bit and verifies that all sent messages were received.
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    topic = "foo/bar"
    host = "localhost"
    port = mqtt_server.port

    mqtt_client_sub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=socket,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
        recv_timeout=5,
    )
    # add_topic_callback() makes sure that the callback will be called only for messages
    # received on the specified topic.
    mqtt_client_sub.add_topic_callback(topic, handle_message)
    logger.info(f"Connecting to MQTT broker (subscriber)")
    mqtt_client_sub.connect()
    logger.info(f"subscribing to {topic}")
    mqtt_client_sub.subscribe(topic)

    sent_msgs = []
    num_msgs = random.randrange(16, 32)
    for i in range(num_msgs):
        logger.debug(f"client {i}")
        rand_time = random.random()
        logger.debug(f"Sleeping for {rand_time}")
        time.sleep(rand_time)

        mqtt_client_pub = MQTT.MQTT(
            broker=host,
            port=port,
            socket_pool=socket,
            ssl_context=ssl.create_default_context(),
            connect_retries=1,
        )
        logger.info(f"Connecting to MQTT broker (publisher {i})")
        mqtt_client_pub.connect()
        logger.info("publishing message")
        message = f"message {i}"
        sent_msgs.append(message)
        mqtt_client_pub.publish(topic, message)
        mqtt_client_pub.disconnect()

    # Wait for the messages to arrive.
    mqtt_client_sub.loop(5)
    mqtt_client_sub.disconnect()

    logger.debug(f"messages received: {len(RECEIVED_MESSAGES)}")
    assert num_msgs == len(RECEIVED_MESSAGES)
    assert set(sent_msgs) == set(RECEIVED_MESSAGES)
