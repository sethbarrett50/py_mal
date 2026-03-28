import pytest

from pydantic import ValidationError


class TestRatSchemas:
    @pytest.mark.unit
    def test_input_event_alias_logic(self):
        """Verify that 'type' alias works for 'event_type'."""
        from rat.common.schemas import InputEvent

        data = {'type': 'click', 'x': 100, 'y': 200}
        event = InputEvent.model_validate(data)
        assert event.event_type == 'click'
        assert event.x == 100

    @pytest.mark.unit
    def test_input_event_serialization(self):
        """Verify serialization uses the alias 'type' for the network protocol."""
        from rat.common.schemas import InputEvent

        event = InputEvent(type='move', x=50, y=50)
        json_output = event.model_dump_json(by_alias=True)
        assert '"type":"move"' in json_output
        assert '"event_type"' not in json_output

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'invalid_data',
        [
            {'type': 'click', 'x': 'not_an_int'},
            {'x': 100, 'y': 100},
        ],
    )
    def test_input_event_validation_errors(self, invalid_data):
        from rat.common.schemas import InputEvent

        with pytest.raises(ValidationError):
            InputEvent.model_validate(invalid_data)
