from .server import Server

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
