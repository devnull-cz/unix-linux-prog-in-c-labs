from .server import Server

import string
import random

import pytest

PROGRAM_PATH = "../mqttserver"


@pytest.fixture
def mqtt_server(request):
    marker = request.node.get_closest_marker("mqtt_server_nofiles")
    if marker:
        nofiles = marker.args[0]
    else:
        nofiles = None
    server = Server(PROGRAM_PATH, nofiles=nofiles)
    server.start()
    yield server
    server.stop()


def randomword(length):
    """
    :param length: number of letters
    :return: random string of lowercase ASCII characters
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
