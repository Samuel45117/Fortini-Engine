"""Logging system for Fortini Engine."""

import logging
import sys
from datetime import datetime
from pathlib import Path


class Logger:
    """Centralized logging system for the engine."""

    _instance = None
    _loggers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.log_dir = Path.home() / "Fortini Documents" / "Logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup main logger
        self._setup_main_logger()

    def _setup_main_logger(self):
        """Setup the main logger with file and console handlers."""
        self.main_logger = logging.getLogger("FortiniEngine")
        self.main_logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # File handler
        log_file = (
            self.log_dir
            / f"fortini_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        self.main_logger.addHandler(console_handler)
        self.main_logger.addHandler(file_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger for a specific module."""
        if name not in self._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            self._loggers[name] = logger
        return self._loggers[name]

    def info(self, message: str) -> None:
        """Log info message."""
        self.main_logger.info(message)

    def debug(self, message: str) -> None:
        """Log debug message."""
        self.main_logger.debug(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        self.main_logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message."""
        self.main_logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message."""
        self.main_logger.critical(message)
