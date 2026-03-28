import pytest


@pytest.mark.unit
def test_executor_full_range(mocker):
    from rat.common.schemas import InputEvent
    from rat.server.executor import InputExecutor

    mock_move = mocker.patch('pyautogui.moveTo')
    mock_click = mocker.patch('pyautogui.click')

    InputExecutor.execute(InputEvent(type='move', x=10, y=20))
    mock_move.assert_called_with(10, 20, _pause=False)

    InputExecutor.execute(InputEvent(type='click', x=100, y=100, button='right'))
    mock_click.assert_called_with(100, 100, button='right')
