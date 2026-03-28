import pytest


@pytest.fixture
def screen_event():
    from rat.common.schemas import InputEvent

    return InputEvent(type='click', x=100, y=200, button='left')
