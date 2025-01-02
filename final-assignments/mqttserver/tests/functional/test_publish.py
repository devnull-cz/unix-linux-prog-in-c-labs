import logging
import socket
import ssl
import time
import random

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server


def handle_message(mqtt_client, topic, message):
    print(f"got msg on {topic}: {message}")
    mqtt_client.user_data.append(message)


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

    received_msgs = []
    pool = socket
    mqtt_client_sub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
        recv_timeout=5,
        user_data=received_msgs,
    )

    # add_topic_callback() makes sure that the callback will be called only for messages
    # received on the specified topic.
    mqtt_client_sub.add_topic_callback(topic, handle_message)
    logger.info(f"Connecting to MQTT broker (subscriber)")
    mqtt_client_sub.connect(session_id="client_sub")
    logger.info(f"subscribing to {topic}")
    mqtt_client_sub.subscribe(topic)

    sent_msgs = []
    num_msgs = random.randrange(16, 32)
    logger.info(f"will send {num_msgs}")
    for i in range(num_msgs):
        logger.debug(f"client {i}")
        rand_time = random.random()
        logger.debug(f"Sleeping for {rand_time}")
        time.sleep(rand_time)

        pool = socket
        mqtt_client_pub = MQTT.MQTT(
            broker=host,
            port=port,
            socket_pool=pool,
            ssl_context=ssl.create_default_context(),
            connect_retries=1,
        )

        logger.info(f"Connecting to MQTT broker (publisher {i})")
        mqtt_client_pub.connect(session_id="client_pub")
        logger.info("publishing message")
        message = f"message {i}"
        sent_msgs.append(message)
        mqtt_client_pub.publish(topic, message)
        mqtt_client_pub.disconnect()

    # Wait for the messages to arrive.
    logger.info("waiting for the messages to arrive for 5 seconds")
    mqtt_client_sub.loop(5)

    logger.info("disconnecting")
    mqtt_client_sub.disconnect()

    logger.debug(f"messages received: {len(received_msgs)}")
    logger.debug(f"messages sent: {len(sent_msgs)}")
    assert num_msgs == len(
        received_msgs
    ), "number of sent messages is not equal to the number of received messages"
    assert set(sent_msgs) == set(
        received_msgs
    ), "sets of sent and received messages are not equal"
