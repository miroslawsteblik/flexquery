import click
import logging
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from flexquery.config.pathconfig import  AppPaths


class ClickEchoHandler(logging.StreamHandler):
    """Custom logging handler that uses Click's echo for terminal output"""
    
    def emit(self, record):
        try:
            msg = self.format(record)
            
            # Style output based on log level
            if record.levelno >= logging.ERROR:
                click.secho(msg, fg="red", err=True, bold=True)
            elif record.levelno >= logging.WARNING:
                click.secho(msg, fg="yellow")
            elif record.levelno == logging.INFO:
                click.echo(msg)
            elif record.levelno == logging.DEBUG:
                click.secho(msg, dim=True)
                
        except Exception:
            self.handleError(record)

def initialize_logging():
    """Initialize the logging system with console, file, and archive handlers."""

    root_logger = logging.getLogger()
    
    # Clear any existing handlers (important for avoiding duplicate logs)
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    # Set the root logger level to DEBUG to capture all messages
    root_logger.setLevel(logging.DEBUG)
    
    # File handler - rotates daily
    file_handler = TimedRotatingFileHandler(AppPaths.get_log_filepath(), when='midnight', interval=1)
    file_formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG) # Log all messages to file
    
    # Archive handler - this accumulates all logs
    archive_handler = logging.FileHandler(AppPaths.get_log_archive_filepath(), mode='a')
    archive_handler.setLevel(logging.DEBUG) # Log all messages to archive
    archive_formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    archive_handler.setFormatter(archive_formatter)

    # Click-based console handler
    console_handler = ClickEchoHandler()
    console_formatter = logging.Formatter("%(message)s")  
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)  
    
    # Add handlers to the root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(archive_handler)
    
    # Avoid propagation to default handlers
    logging.basicConfig(handlers=[])
    
    return root_logger

def get_logger(name=None):
    """Get a logger with the specified name."""
    if name:
        return logging.getLogger(name)
    return logging.getLogger()

def _log_message(message):
    """Helper function for logging messages."""
    logger = get_logger()
    logger.debug(message)

def log_execution(func):
    """Decorator to log the execution of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            className = args[0].__class__.__name__ if args else ''
        except (IndexError, AttributeError):
            className = 'Function'
            
        functionName = func.__name__

        _log_message(f"Launching {className}.{functionName}")

        try:
            result = func(*args, **kwargs)
            _log_message(f"Completed {className}.{functionName}")
            return result
        except Exception as e:
            _log_message(f"Error in {className}.{functionName}: {e.__class__.__name__}")
            raise e
    return wrapper

def log_separator(env=None):
    """Simple log separator."""
    env_str = f" [ENV: {env}]" if env else ""
    logger = get_logger()
    logger.info("\n" + "=" * 40 + f" NEW EXECUTION{env_str} " + "=" * 40 + "\n")



