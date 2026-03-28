import pytest


@pytest.mark.smoke
def test_mss_availability():
    import mss

    with mss.mss() as sct:
        assert len(sct.monitors) > 0


@pytest.mark.smoke
def test_pygame_init():
    import pygame

    success, fail = pygame.init()
    assert fail == 0


@pytest.mark.smoke
def test_server_instantiation():
    from rat.server.stream import ScreenServer

    srv = ScreenServer('127.0.0.1', 5555)
    assert srv.host == '127.0.0.1'
