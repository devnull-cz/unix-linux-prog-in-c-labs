# The version should be bumped for each non-trivial change.
VERSION = "0.5"

import sys

if not sys.implementation.name == "circuitpython":
    from typing import Optional

    from circuitpython_typing.socket import (
        SocketType,
        SSLContextType,
    )


class FakeConnectionManager:
    """
    Fake ConnectionManager class used to subvert the socket pooling mechanism so that we can get multiple distinct
    connections to the same broker after MiniMQTT switched to ConnectionManager.
    """

    def __init__(self, socket_pool):
        self._socket_pool = socket_pool

    def get_socket(
        self,
        host: str,
        port: int,
        proto: str,
        session_id: Optional[str] = None,
        *,
        timeout: float = 1.0,
        is_ssl: bool = False,
        ssl_context: Optional[SSLContextType] = None,
    ) -> SocketType:
        """
        Replicate what the ConnectionManager does and what MiniMQTT was doing previously by itself.
        """

        addr_info = self._socket_pool.getaddrinfo(
            host, port, 0, self._socket_pool.SOCK_STREAM
        )[0]

        socket = self._socket_pool.socket(addr_info[0], addr_info[1])
        connect_host = addr_info[-1][0]

        socket.settimeout(timeout)

        socket.connect((connect_host, port))

        return socket

    def close_socket(self, socket) -> None:
        socket.close()
