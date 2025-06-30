import sys
import logging
from pathlib import Path
from colorlog import ColoredFormatter

def setup_logger(log_name: str, log_path: Path) -> logging.Logger:
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    logger.propagate = False

    if not logger.handlers:
        color_formatter = ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s] %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)

    return logger
