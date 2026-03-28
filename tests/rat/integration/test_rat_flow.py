import socket
import threading
import time

import pytest


@pytest.mark.integration
def test_screen_server_connection():
    from rat.server.stream import ScreenServer

    server = ScreenServer(host='127.0.0.1', port=5556)

    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(1)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = client_sock.connect_ex(('127.0.0.1', 5556))

    assert result == 0
    client_sock.close()
