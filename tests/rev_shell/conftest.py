import pytest


@pytest.fixture
def shell_config():
    from rev_shell.config import ShellConfig

    """Matches the ShellConfig Pydantic model for rev_shell."""
    return ShellConfig(host='127.0.0.1', port=4444, log_file='test.log')


@pytest.fixture
def mock_socket(mocker):
    """Mocks a standard socket for network testing."""
    mock_sock = mocker.patch('socket.socket')
    instance = mock_sock.return_value
    instance.__enter__.return_value = instance
    return instance
