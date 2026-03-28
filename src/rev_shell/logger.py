import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(log_file: str) -> logging.Logger:
    logger = logging.getLogger('vps_shell')
    logger.setLevel(logging.INFO)

    log_path = Path(log_file).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
