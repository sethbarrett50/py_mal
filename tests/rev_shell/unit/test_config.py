import pytest

from pydantic import ValidationError


class TestRevShellConfig:
    @pytest.mark.unit
    def test_default_config(self):
        """Verify defaults are applied when no arguments are passed."""
        from rev_shell.config import ShellConfig

        config = ShellConfig()
        assert config.host == '127.0.0.1'
        assert config.port == 4444
        assert 'rev_shell.log' in config.log_file

    @pytest.mark.unit
    def test_custom_config(self):
        """Verify custom values override defaults."""
        from rev_shell.config import ShellConfig

        config = ShellConfig(host='1.2.3.4', port=8080, log_file='custom.log')
        assert config.host == '1.2.3.4'
        assert config.port == 8080
        assert config.log_file == 'custom.log'

    @pytest.mark.unit
    def test_invalid_port(self):
        """Verify that out-of-range ports raise a ValidationError."""
        from rev_shell.config import ShellConfig

        with pytest.raises(ValidationError):
            ShellConfig(port=999999)
