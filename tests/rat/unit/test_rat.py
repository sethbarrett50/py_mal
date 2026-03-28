import struct

from unittest.mock import MagicMock

import pytest


class TestScreenServerLogic:
    @pytest.mark.unit
    def test_packet_header_structure(self):
        from rat.common.schemas import PacketType

        frame_size = 1024
        header = struct.pack('>BL', PacketType.FRAME, frame_size)

        p_type, size = struct.unpack('>BL', header)
        assert p_type == 1
        assert size == 1024

    @pytest.mark.unit
    def test_input_event_serialization(self, screen_event):
        json_data = screen_event.model_dump_json(by_alias=True)
        assert '"type":"click"' in json_data
        assert '"x":100' in json_data

    @pytest.mark.unit
    def test_screen_handler_compression(self, mocker):
        from rat.server.capture import ScreenHandler

        mock_mss = mocker.patch('mss.mss')
        mock_instance = mock_mss.return_value.__enter__.return_value
        mock_instance.monitors = [None, {'top': 0, 'left': 0, 'width': 100, 'height': 100}]

        mock_img = MagicMock()
        mock_img.size = (100, 100)
        mock_img.bgra = b'\x00' * (100 * 100 * 4)
        mock_instance.grab.return_value = mock_img

        from PIL import Image

        real_fake_img = Image.new('RGB', (100, 100))
        mocker.patch('PIL.Image.frombytes', return_value=real_fake_img)

        handler = ScreenHandler()
        frame = handler.get_frame(quality=10)
        assert isinstance(frame, bytes)
