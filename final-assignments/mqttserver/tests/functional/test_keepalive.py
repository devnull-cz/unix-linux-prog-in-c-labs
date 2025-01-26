import logging
import socket
import ssl
import time
import pytest

import adafruit_minimqtt.adafruit_minimqtt as MQTT

from ..common import mqtt_server


# Run multiple times to catch potentially erroneous reuse of client structures on the server.
@pytest.mark.parametrize("keep_alive_timeout", [8, 16])
def test_keepalive(mqtt_server, keep_alive_timeout):
    """
    Connect with a particular keep alive timeout, sleep for double the keep alive timeout, send PINGREQ.
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
        keep_alive=keep_alive_timeout,
    )

    logger.debug(f"connecting with keep alive = {keep_alive_timeout}")
    mqtt_client.connect()
    ensure_keep_alive(keep_alive_timeout, logger, mqtt_client)


def ensure_keep_alive(keep_alive_timeout, logger, mqtt_client):
    """
    Sleep 2 * keep_alive_timeout and then send PINGREQ.
    """
    # The MQTT spec says not hearing from the client for 1.5 times keep alive timeout
    # means it can be considered dead and disconnected.
    sleep_period = 2 * keep_alive_timeout
    logger.debug(f"sleeping for {sleep_period} seconds")
    time.sleep(sleep_period)
    try:
        # Will wait for the PINGRESP message for keep_alive seconds. Should not get anything back.
        # While on Linux this raises MMQTTException (Unable to receive 1 bytes within 8 seconds.),
        # on macOS this leads to ConnectionResetError or BrokenPipeError.
        with pytest.raises((MQTT.MMQTTException, ConnectionResetError, BrokenPipeError)):
            logger.debug("pinging the server")
            mqtt_client.ping()
    finally:
        # Cleanup so the socket is cleared in the ConnectionManager pool used by MiniMQTT.
        mqtt_client.disconnect()
