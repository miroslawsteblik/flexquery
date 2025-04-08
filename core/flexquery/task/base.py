from typing import Any, Dict, Optional
from flexquery.config.logging_config import get_logger, initialize_logging, log_separator
from flexquery.config.exceptions import TaskExecutionError

logger = get_logger(__name__)

class Task:
    """Base class for all FlexQuery tasks.
    
    Provides a template method pattern for task execution with hooks for setup,
    validation, execution, and cleanup.
    """
    
    def __init__(self, *args, **kwargs):
        initialize_logging()
        log_separator()
        
        self._args = args
        self._kwargs = kwargs
        self._status = "initialized"
        self._result = None
        
    @property
    def status(self) -> str:
        """Get the current status of the task."""
        return self._status
        
    @property
    def result(self) -> Any:
        """Get the result of the task execution."""
        return self._result
        
    def validate(self) -> bool:
        """
        Validate task parameters before execution.
        
        Returns:
            bool: True if parameters are valid
            
        Raises:
            ValueError: If parameters are invalid
        """
        return True
        
    def setup(self) -> bool:
        """
        Perform any setup needed before execution.
        
        Returns:
            bool: True if setup was successful
        """
        return True
        
    def _execute(self) -> Any:
        """
        Task-specific execution logic to be implemented by subclasses.
        
        Returns:
            Any: Result of the task execution
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement this method")
        
    def cleanup(self) -> None:
        """Cleanup resources after task execution."""
        pass
        
    def execute(self) -> Any:
        """
        Execute the task with standard lifecycle management.
        
        Returns:
            Any: Result of the task execution
            
        Raises:
            TaskExecutionError: If task execution fails
        """
        try:
            # Update status
            self._status = "validating"
            logger.debug(f"Validating task {self.__class__.__name__}")
            
            # Validate
            if not self.validate():
                self._status = "invalid"
                logger.error(f"Task {self.__class__.__name__} validation failed")
                raise TaskExecutionError("Task validation failed")
                
            # Setup
            self._status = "setting_up"
            logger.debug(f"Setting up task {self.__class__.__name__}")
            if not self.setup():
                self._status = "setup_failed"
                logger.error(f"Task {self.__class__.__name__} setup failed")
                raise TaskExecutionError("Task setup failed")
                
            # Execute
            self._status = "executing"
            logger.debug(f"Executing task {self.__class__.__name__}")
            self._result = self._execute()
            self._status = "completed"
            logger.debug(f"Task {self.__class__.__name__} completed successfully")
            
            return self._result
            
        except Exception as e:
            self._status = "failed"
            logger.error(f"Task {self.__class__.__name__} failed: {str(e)}")
            raise TaskExecutionError(f"Task execution failed: {str(e)}") from e
            
        finally:
            # Always perform cleanup
            logger.debug(f"Cleaning up task {self.__class__.__name__}")
            self.cleanup()