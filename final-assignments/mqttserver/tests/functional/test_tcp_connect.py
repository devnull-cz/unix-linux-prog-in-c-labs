import socket

from ..common import mqtt_server


def test_connect_v4_v6(mqtt_server):
    """
    See if the server supports both IPv4 and IPv6.
    """
    print("IPv4")
    socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    socket_v4.connect(("localhost", mqtt_server.port))
    socket_v4.close()

    print("IPv6")
    socket_v6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    socket_v6.connect(("localhost", mqtt_server.port, 0, 0))
    socket_v6.close()
