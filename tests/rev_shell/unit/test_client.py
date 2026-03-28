from unittest.mock import MagicMock

import pytest


class TestShellClient:
    @pytest.mark.unit
    def test_execute_success(self, shell_config, mocker):
        from rev_shell.client import ShellClient

        mocker.patch('subprocess.check_output', return_value=b'success_output')
        client = ShellClient(shell_config, MagicMock())

        result = client._execute('ls')
        assert result == b'success_output'

    @pytest.mark.unit
    def test_execute_failure(self, shell_config, mocker):
        from subprocess import CalledProcessError

        from rev_shell.client import ShellClient

        mocker.patch('subprocess.check_output', side_effect=CalledProcessError(1, 'cmd', output=b'err'))
        client = ShellClient(shell_config, MagicMock())

        result = client._execute('bad_cmd')
        assert result == b'err'

    @pytest.mark.timeout(5)
    @pytest.mark.unit
    def test_start_connection_refused(self, shell_config, mock_socket, mocker):
        from rev_shell.client import ShellClient

        mock_sleep = mocker.patch('rev_shell.client.time.sleep')

        mock_socket.connect.side_effect = ConnectionRefusedError()

        mock_logger = MagicMock()
        client = ShellClient(shell_config, mock_logger)

        client.start(max_retries=2)

        mock_logger.warning.assert_called_with('Connection failed. Retrying in 10s...')
        assert mock_sleep.call_count == 1

    @pytest.mark.unit
    @pytest.mark.parametrize('cmd', ['exit', 'quit', 'EXIT'])
    def test_loop_break_on_exit(self, shell_config, mock_socket, mocker, cmd):
        from rev_shell.client import ShellClient

        mock_socket.recv.return_value = cmd.encode()
        logger = MagicMock()
        client = ShellClient(shell_config, logger)

        client.start()
        assert mock_socket.close.called
