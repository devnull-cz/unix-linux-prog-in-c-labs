# The version should be bumped for each non-trivial change.
VERSION = "0.8"

import sys

if not sys.implementation.name == "circuitpython":
    from typing import Optional

    from circuitpython_typing.socket import (
        SocketType,
        SSLContextType,
    )
