import pytest

from click.testing import CliRunner


@pytest.mark.unit
class TestRatCLI:
    def test_rat_server_command(self, mocker):
        from rat.cli import main

        mock_server = mocker.patch('rat.cli.ScreenServer')
        mock_instance = mock_server.return_value

        runner = CliRunner()
        result = runner.invoke(main, ['server'])

        assert result.exit_code == 0
        mock_server.assert_called_once_with('0.0.0.0', 5555)
        assert mock_instance.start.called

    def test_rat_client_command(self, mocker):
        from rat.cli import main

        mock_viewer = mocker.patch('rat.cli.RemoteViewer')
        mock_instance = mock_viewer.return_value

        runner = CliRunner()
        result = runner.invoke(main, ['client', '--host', '127.0.0.1'])

        assert result.exit_code == 0
        mock_viewer.assert_called_once_with('127.0.0.1', 5555)
        assert mock_instance.run.called

    def test_rat_client_missing_host(self):
        from rat.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ['client'])

        assert result.exit_code != 0
        assert "Missing option '--host'" in result.output
