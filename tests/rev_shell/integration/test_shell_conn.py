import socket
import threading
import time

import pytest


def run_fake_server(host, port, command, response_queue):
    """A minimal TCP server to simulate the C2 listener."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        conn, _addr = s.accept()
        with conn:
            conn.sendall(command.encode('utf-8'))
            data = conn.recv(4096)
            response_queue.append(data.decode('utf-8'))
            conn.sendall(b'exit')


@pytest.mark.integration
@pytest.mark.timeout(10)
def test_full_command_execution(mocker):

    from rev_shell.client import ShellClient
    from rev_shell.config import ShellConfig

    host = '127.0.0.1'
    port = 55556
    test_command = "echo 'integration_test'"
    responses = []

    server_thread = threading.Thread(target=run_fake_server, args=(host, port, test_command, responses))
    server_thread.start()

    time.sleep(0.2)

    config = ShellConfig(host=host, port=port)
    mock_logger = mocker.MagicMock()
    client = ShellClient(config, mock_logger)

    client.start(max_retries=1)

    server_thread.join()
    assert len(responses) > 0
    assert 'integration_test' in responses[0]
