import pytest


@pytest.mark.unit
@pytest.mark.parametrize(
    'cmd, expected',
    [
        ('echo hello', b'hello'),
        ('bad_cmd', b'not found'),
    ],
)
def test_shell_execution(shell_config, mock_logger, mocker, cmd, expected):
    from rev_shell.client import ShellClient

    mock_run = mocker.patch('subprocess.check_output', return_value=expected)

    client = ShellClient(shell_config, mock_logger)
    result = client._execute(cmd)

    assert result == expected
    mock_run.assert_called_once()
