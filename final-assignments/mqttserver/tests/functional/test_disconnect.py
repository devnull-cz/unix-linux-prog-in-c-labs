import logging
import socket
import ssl
import pytest

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server


def test_disconnect(mqtt_server):
    """
    Connect, send PING message to the server, send DISCONNECT, send PING once again.
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

    logger.debug("connecting to server")
    mqtt_client.connect()
    # Will wait for PINGRESP for keep_alive seconds.
    logger.debug("pinging the server")
    mqtt_client.ping()
    logger.debug("disconnecting from the server")
    mqtt_client.disconnect()
    with pytest.raises(MQTT.MMQTTException) as e_info:
        logger.debug("pinging the server once again")
        mqtt_client.ping()
    assert "not connected" in str(e_info.value)
