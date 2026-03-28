import io
import socket
import struct

import pygame

from rat.common.schemas import InputEvent


class RemoteViewer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pygame.init()

    def _send_input(self, event: InputEvent):
        """Packs and sends an input event to the server."""
        data = event.model_dump_json().encode('utf-8')
        header = struct.pack('>L', len(data))
        self.socket.sendall(header + data)

    def run(self):
        self.socket.connect((self.host, self.port))
        screen = None
        clock = pygame.time.Clock()

        while True:
            header_data = self.socket.recv(5)
            if not header_data:
                break
            p_type, size = struct.unpack('>BL', header_data)

            img_bytes = b''
            while len(img_bytes) < size:
                chunk = self.socket.recv(min(size - len(img_bytes), 8192))
                if not chunk:
                    break
                img_bytes += chunk

            try:
                image = pygame.image.load(io.BytesIO(img_bytes))
                if screen is None:
                    screen = pygame.display.set_mode(image.get_size())
                    pygame.display.set_caption(f'VPS Remote Desktop: {self.host}')

                screen.blit(image, (0, 0))
                pygame.display.flip()
            except Exception:
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self._send_input(InputEvent(type='click', x=x, y=y, button='left'))
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self._send_input(InputEvent(type='key', key_code=key_name))

            clock.tick(60)
