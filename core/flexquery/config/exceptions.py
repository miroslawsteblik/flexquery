class ConfigurationError(Exception):
    """Raised when there's an issue with the configuration."""
    def __init__(self, message, filepath=None, **context):
        self.filepath = filepath
        self.context = context
        super().__init__(message)
    
    def __str__(self):
        msg = super().__str__()
        if self.filepath:
            msg += f" (file: {self.filepath})"
        return msg

class DatabaseConnectionError(Exception):
    """Raised when a database connection cannot be established."""
    pass

class DataProcessorError(Exception):
    """Raised when an error occurs during data processing."""
    pass

class SQLQueryError(Exception):
    """Raised when an error occurs during SQL query execution."""
    pass

class ApplicationError(Exception):
    """Raised when an application error occurs."""
    pass

class BrowserError(Exception):
    """Raised when an error occurs while opening a browser."""
    pass

class TaskExecutionError(Exception):
    """Raised when an error occurs during task execution."""
    pass





