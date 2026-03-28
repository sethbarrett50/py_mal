import importlib

import pytest

from click.testing import CliRunner


@pytest.mark.smoke
class TestRevShellHealth:
    """Basic health checks for the rev_shell component."""

    @pytest.mark.parametrize(
        'module_name', ['rev_shell.client', 'rev_shell.config', 'rev_shell.logger', 'rev_shell.cli']
    )
    def test_imports(self, module_name):
        """Verify all core modules can be imported without errors."""
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            pytest.fail(f'Failed to import {module_name}: {e}')

    def test_cli_help(self):
        """Verify the CLI exists and shows the help menu."""
        from rev_shell.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ['--help'])

        assert result.exit_code == 0
        assert 'Listener IP' in result.output
        assert 'Listener Port' in result.output

    def test_config_defaults(self):
        """Verify the ShellConfig can be instantiated with defaults."""
        from rev_shell.config import ShellConfig

        config = ShellConfig()
        assert config.host is not None
        assert isinstance(config.port, int)
