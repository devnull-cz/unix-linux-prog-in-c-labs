import logging
import socket
import ssl

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server


def test_ping(mqtt_server):
    """
    Connect, send PING message to the server, wait for the response.
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    host = "localhost"
    port = mqtt_server.port

    mqtt_client = MQTT.MQTT(
        broker=host,
        port=port,
        socket_pool=socket,
        ssl_context=ssl.create_default_context(),
        connect_retries=1,
        recv_timeout=5,
        keep_alive=2,
    )

    mqtt_client.connect()
    # Will wait for PINGRESP for keep_alive seconds.
    mqtt_client.ping()
    # cleanup
    mqtt_client.disconnect()
