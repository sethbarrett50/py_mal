import pytest


@pytest.mark.integration
def test_end_to_end_event_injection(mocker):
    from rat.common.schemas import InputEvent
    from rat.server.executor import InputExecutor

    mock_gui = mocker.patch('pyautogui.click')

    event = InputEvent(type='click', x=500, y=500, button='right')
    payload = event.model_dump_json()

    received_event = InputEvent.model_validate_json(payload)
    InputExecutor.execute(received_event)

    mock_gui.assert_called_once_with(500, 500, button='right')
