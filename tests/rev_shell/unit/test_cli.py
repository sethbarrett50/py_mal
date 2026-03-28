import pytest

from click.testing import CliRunner


@pytest.mark.unit
def test_rev_shell_cli_success(mocker):
    from rev_shell.cli import main

    mock_config = mocker.patch('rev_shell.cli.ShellConfig')
    _mock_logger = mocker.patch('rev_shell.cli.setup_logger')
    mock_client_class = mocker.patch('rev_shell.cli.ShellClient')
    mock_client_instance = mock_client_class.return_value

    runner = CliRunner()
    result = runner.invoke(main, ['--host', '1.2.3.4', '--port', '9999'])

    assert result.exit_code == 0
    mock_config.assert_called_once_with(host='1.2.3.4', port=9999)
    assert mock_client_instance.start.called


@pytest.mark.unit
def test_rev_shell_cli_error(mocker):
    from rev_shell.cli import main

    mocker.patch('rev_shell.cli.ShellConfig', side_effect=ValueError('Invalid Port'))

    runner = CliRunner()
    result = runner.invoke(main, ['--port', 'not-a-number'])

    assert 'Configuration Error' in result.output
