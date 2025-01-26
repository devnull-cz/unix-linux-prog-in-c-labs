import logging
import random
import socket
import ssl

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server, randomword


def handle_message(client, topic, message):
    print(f"{topic}: {message}")
    received_messages = client.user_data
    assert received_messages is not None
    if received_messages.get(topic) is None:
        received_messages[topic] = []

    received_messages[topic].append(message)


def test_unsubscribe(mqtt_server):
    """
    1. client 1: connect, subscribe to one a topic
    2. client 2: connect, start publishing messages to a set of topics,
                 including the topic subscribed by the first client
    3. client 1: unsubscribe during the sequence of messages published to the topic
    4. Check that the client received only the messages published before unsubscribing.
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
        socket_timeout=0.1,
        user_data=received_messages,
    )

    logger.info(f"Connecting to MQTT broker (subscriber)")
    mqtt_client_sub.connect(session_id="client_sub")
    subscribed_topic = "foo/bar"
    # add_topic_callback() makes sure that the callback will be called only for messages
    # received on the specified topic.
    mqtt_client_sub.add_topic_callback(subscribed_topic, handle_message)
    mqtt_client_sub.subscribe(subscribed_topic)

    mqtt_client_pub = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
    )

    logger.info(f"Connecting to MQTT broker (publisher)")
    mqtt_client_pub.connect(session_id="client_pub")

    # The number of messages and topics is chosen with respect to the default pytest timeout of 60 seconds.
    message_count = 30
    sent_msgs = list()
    expected_msgs = list()
    unsubscribed = False
    topics = ["foo", "bar", subscribed_topic, "bar/bar"]
    for topic in topics:
        for i in range(message_count):
            msg = randomword(random.randrange(10, 30))
            logger.debug(f"Publishing message {i} to {topic}: {msg}")
            mqtt_client_pub.publish(topic, msg)
            sent_msgs.append(msg)

            if topic == subscribed_topic and not unsubscribed:
                expected_msgs.append(msg)

            # Wait for the messages to arrive.
            mqtt_client_sub.loop(0.1)

            if i == message_count // 2 and topic == subscribed_topic:
                logger.info(f"Unsubscribing from topic {topic} (subscriber)")
                mqtt_client_sub.unsubscribe(subscribed_topic)
                unsubscribed = True

    logger.info("Checking messages received")
    try:
        topic_msgs = received_messages[subscribed_topic]
        assert topic_msgs
        logger.debug(
            f"number of messages received for topic {topic}: {len(topic_msgs)}"
        )
        assert len(expected_msgs) == len(topic_msgs)
        assert expected_msgs == topic_msgs
        assert set(received_messages.keys()) == {subscribed_topic}
    finally:
        mqtt_client_sub.disconnect()
        mqtt_client_pub.disconnect()
