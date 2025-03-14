import logging
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
import os


# Log file paths
log_path = "flexquery/log/data_processor.log"
log_archive_path = "flexquery/log/data_processor.log.archive"


def initialize_logging():
    """Initialize the logging system with console, file, and archive handlers."""

    root_logger = logging.getLogger()
    
    # Clear any existing handlers (important for avoiding duplicate logs)
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Main log file - rotates daily, keeps 1 backup
    file_handler = TimedRotatingFileHandler(
        log_path,
        when='midnight',  # Rotate at midnight
        interval=1,       # Daily rotation
        backupCount=1     # Keep only 1 day of logs in the active file
    )
    file_handler.setLevel(logging.INFO)
    
    # Archive handler - this accumulates all logs
    archive_handler = logging.FileHandler(log_archive_path, mode='a')
    archive_handler.setLevel(logging.INFO)
    
    # Set formatter for all handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    archive_handler.setFormatter(formatter)
    
    # Add handlers to the root logger
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(archive_handler)
    
    # Avoid propagation to default handlers
    logging.basicConfig(handlers=[])
    
    return root_logger

root_logger = initialize_logging()

def get_logger(name=None):
    """Get a logger with the specified name."""
    if name:
        return logging.getLogger(name)
    return root_logger

def _log_message(message):
    """Helper function for logging messages."""
    root_logger.info(message)

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        className = args[0].__class__.__name__ if args else ''
        functionName = func.__name__
        _log_message(f"Launching {className}.{functionName}")
        try:
            result = func(*args, **kwargs)
            _log_message(f"Completed {className}.{functionName}")
            return result
        except Exception as e:
            root_logger.error(f"Error in {className}.{functionName}: {e}")
            raise

    return wrapper

def log_separator(env=None):
    """Simple log separator."""
    env_str = f" [ENV: {env}]" if env else ""
    root_logger.info("\n" + "=" * 40 + f" NEW EXECUTION{env_str} " + "=" * 40 + "\n")
