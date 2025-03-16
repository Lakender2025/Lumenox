import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configures logging for the Flask app."""
    log_file = "app_debug.log"
    
    # Create a logger
    logger = logging.getLogger("flask_app")
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs messages to a file
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Define log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger

# Create a logger instance
logger = setup_logger()
