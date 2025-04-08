from flexquery.task.base import Task
from flexquery.config.logging_config import get_logger
from flexquery.config.pathconfig import  AppPaths
from flexquery.utils import skeleton

logger = get_logger(__name__)

class InitTask(Task):
    """Task for initializing FlexQuery configuration and project structure."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._env = kwargs.get("env", None)
    
    @property
    def env(self):
        """Environment getter."""
        return self._env
    
    @env.setter
    def env(self, value):
        """Environment setter."""
        self._env = value

    def validate(self):
        """Validate initialization requirements."""
        return True
        
    def setup(self):
        """Prepare for initialization."""
        dirs = AppPaths.ensure_directories()
        return True
        
    def _execute(self):
        """Execute the initialization logic."""
        try:
            skeleton.create_profiles_template()

            if self.env:
                # Initialize the environment directories and templates
                skeleton.initialize_env_directories(self.env)
                skeleton.create_params_template(self.env)
                skeleton.create_sql_template(self.env)
            else:
                # If no environment specified, initialize default TEST environment
                default_env = "TEST"
                logger.info(f"No environment specified, initializing default: {default_env}")
                skeleton.initialize_env_directories(default_env)
                skeleton.create_params_template(default_env)
                skeleton.create_sql_template(default_env)

            logger.info("Initialization complete!")
            return True
        
        except FileExistsError as e:
            logger.warning(f"Some files already exist: {e}")
            return True  
            
        except PermissionError as e:
            logger.error(f"Permission error during initialization: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Error initializing project: {e}")
            return False
            
