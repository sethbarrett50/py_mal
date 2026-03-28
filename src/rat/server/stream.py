import logging
import socket
import struct
import threading

from rat.common.schemas import InputEvent, PacketType

from .capture import ScreenHandler
from .executor import InputExecutor

logger = logging.getLogger(__name__)


class ScreenServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.capture = ScreenHandler()
        self.executor = InputExecutor()
        self._running = True

    def stop(self):
        """Signals the server loops to terminate."""
        self._running = False

    def _listen_for_inputs(self, conn: socket.socket):
        """Threaded listener for client mouse/keyboard events."""
        conn.settimeout(1.0)
        while self._running:
            try:
                raw_size = conn.recv(4)
                if not raw_size:
                    break
                size = struct.unpack('>L', raw_size)[0]

                payload = conn.recv(size).decode('utf-8')
                event = InputEvent.model_validate_json(payload)
                self.executor.execute(event)
            except (socket.timeout, ConnectionResetError):
                continue
            except Exception as e:
                logger.debug(f'Input listener error: {e}')
                break

    def start(self):
        """Starts the main streaming server loop."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            s.settimeout(1.0)
            s.bind((self.host, self.port))
            s.listen(1)
            print(f'[*] Screen Server active on {self.host}:{self.port}')

            while self._running:
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    continue

                with conn:
                    print(f'[*] Accepted connection from {addr}')
                    input_thread = threading.Thread(target=self._listen_for_inputs, args=(conn,), daemon=True)
                    input_thread.start()

                    while self._running:
                        try:
                            frame = self.capture.get_frame()
                            header = struct.pack('>BL', PacketType.FRAME, len(frame))
                            conn.sendall(header + frame)
                        except (ConnectionResetError, BrokenPipeError):
                            print('[!] Client disconnected.')
                            break
                        except Exception as e:
                            logger.error(f'Stream error: {e}')
                            break
