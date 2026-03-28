import pyautogui

from rat.common.schemas import InputEvent

pyautogui.FAILSAFE = False


class InputExecutor:
    @staticmethod
    def execute(event: InputEvent) -> None:
        try:
            if event.event_type == 'move':
                pyautogui.moveTo(event.x, event.y, _pause=False)
            elif event.event_type == 'click':
                pyautogui.click(event.x, event.y, button=event.button)
            elif event.event_type == 'key':
                if event.key_code:
                    pyautogui.press(event.key_code)
        except Exception as e:
            print(f'Execution error: {e}')
