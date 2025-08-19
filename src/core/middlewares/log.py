import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

try:
    from config import LOG_DIR
except ImportError:
    LOG_DIR = Path(__file__).parent.parent.parent.parent / "data" / "logs"


class LoggingSettings:
    def __init__(
        self,
        name: str = "YoBa",
        log_file: str = None,
        console_level: str = "INFO",
        file_level: str = "DEBUG",
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ):

        if log_file is None:
            log_file = str(LOG_DIR / "bot.log")


        os.makedirs(LOG_DIR, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self._file_formatter = logging.Formatter(
            fmt=fmt,
            datefmt=datefmt,
        )



        if colorlog:
            self._console_formatter = colorlog.ColoredFormatter(
                fmt="%(log_color)s" + fmt,
                datefmt=datefmt,
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
                style="%",
            )
        else:
            self._console_formatter = self._file_formatter
            print("colorlog debik")

        if self.logger.handlers:
            self.logger.handlers.clear()

        self.logger.addHandler(self._setup_console_handler(console_level))
        self.logger.addHandler(
            self._setup_file_handler(
                log_file,
                file_level,
                max_bytes,
                backup_count,
            )
        )

    def _setup_console_handler(self, level: str) -> logging.StreamHandler:
        """Coloring console log"""
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(getattr(logging, level.upper()))
        handler.setFormatter(self._console_formatter)
        return handler

    def _setup_file_handler(
        self,
        log_file: str,
        level: str,
        max_bytes: int,
        backup_count: int,
    ) -> RotatingFileHandler:
        """Rotating setting for log-file"""
        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setLevel(getattr(logging, level.upper()))
        handler.setFormatter(self._file_formatter)
        return handler

    def add_handler(self, handler: logging.Handler) -> None:
        """Add custom handler"""
        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        """Get normal logger"""
        return self.logger

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


logger = LoggingSettings().get_logger()
