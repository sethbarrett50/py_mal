import struct

from unittest.mock import MagicMock

import pytest


@pytest.mark.unit
def test_remote_viewer_one_loop_and_exit(mocker):
    from rat.client.viewer import RemoteViewer

    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.display.flip')
    mocker.patch('pygame.image.load')

    mock_sock = mocker.patch('socket.socket').return_value

    fake_header = struct.pack('>BL', 1, 10)
    fake_body = b'fake_image'

    mock_sock.recv.side_effect = [fake_header, fake_body, b'']

    mock_event = MagicMock()
    mock_event.type = 12
    mocker.patch('pygame.event.get', return_value=[mock_event])
    mocker.patch('pygame.time.Clock')

    viewer = RemoteViewer('127.0.0.1', 5555)
    viewer.run()

    assert mock_sock.connect.called
    assert mock_sock.recv.call_count >= 2


@pytest.mark.unit
def test_send_input_packs_correctly(mocker):
    from rat.client.viewer import RemoteViewer
    from rat.common.schemas import InputEvent

    mock_sock = mocker.patch('socket.socket').return_value
    viewer = RemoteViewer('127.0.0.1', 5555)

    event = InputEvent(type='click', x=100, y=200, button='left')
    viewer._send_input(event)

    args, _ = mock_sock.sendall.call_args
    sent_data = args[0]

    header = sent_data[:4]
    payload_len = struct.unpack('>L', header)[0]

    assert payload_len == len(sent_data) - 4
    assert b'click' in sent_data
