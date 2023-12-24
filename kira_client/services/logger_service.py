import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class LoggerService:
    def __init__(
        self,
        log_file_name: str = "kira_client.log",
        max_log_size: int = 5 * 1024 * 1024,
        backup_count: int = 5
    ):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        project_root = os.path.dirname(os.getcwd())
        log_dir = os.path.join(project_root, "logs")

        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        log_file = os.path.join(log_dir, log_file_name)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
