from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_logger():
    """Provides a mock logger to prevent real log files during testing."""
    return MagicMock()
