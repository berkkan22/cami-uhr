import logging
import os


class CustomLogger(logging.Logger):
    def __init__(self, name="backend", level=logging.INFO):
        super().__init__(name, level)
        
        # Ensure the log directory exists
        log_directory = "logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("logs/logfile.log")

        # Custom format to include filename, function name, and line number
        log_format = "%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s"
        formatter = logging.Formatter(log_format)

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers if not already added
        if not self.hasHandlers():
            self.addHandler(console_handler)
            self.addHandler(file_handler)

    # def info(self, msg, *args, **kwargs):
    #     """ Override info() to add file location automatically. """
    #     super().info(f"{msg}", *args, **kwargs)

    # def error(self, msg, *args, **kwargs):
    #     """ Override error() to add file location automatically. """
    #     super().error(f"{msg}", *args, **kwargs)

# Singleton Logger Instance


def get_logger():
    logging.setLoggerClass(CustomLogger)
    return logging.getLogger("backend")
