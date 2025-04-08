import os
import importlib.util
from pathlib import Path
from flexquery.config.exceptions import ConfigurationError
import yaml
from flexquery.config.constants import (
    OUTPUT_DIR_NAME, PROFILES_FILE_NAME, QUERIES_LIBRARY_NAME, LOG_DIR_NAME, LOG_FILE_NAME, LOG_FILE_NAME_ARCHIVE
)

class AppPaths:
    """Class for managing application paths with clear separation between development and installed modes."""
    
    PACKAGE_NAME = 'flexquery'


    @classmethod
    def is_installed_package(cls):
        spec = importlib.util.find_spec(cls.PACKAGE_NAME)
        if not spec:
            return False
        package_path = Path(spec.origin).parent
        return 'site-packages' in str(package_path) or 'dist-packages' in str(package_path)

    @classmethod
    def get_package_path(cls):
        """Get the package path."""
        package = importlib.import_module(cls.PACKAGE_NAME)
        package_path = Path(package.__file__).parent.resolve()
        return package_path

    @classmethod
    def get_project_root(cls):
        """Get the root directory of the project."""
        package_path = cls.get_package_path()
        if cls.is_installed_package():
            # In installed mode, return the package directory
            site_packages = package_path.parent
            venv_path = site_packages.parent.parent
            return venv_path.parent
        else:
            # In development mode, return the project root
            package_path = package_path.parent.parent
            return package_path
        
    @classmethod
    def get_output_dir(cls):
        """Get the output directory."""
        return cls.get_project_root() / OUTPUT_DIR_NAME
    
    @classmethod
    def get_queries_lib_dir(cls):
        """Get the queries library directory."""
        return cls.get_project_root() / QUERIES_LIBRARY_NAME
    
    @classmethod
    def get_log_dir(cls, create: bool = False):
        """Get the log directory."""
        log_path = cls.get_project_root() / LOG_DIR_NAME
        if create and not log_path.exists():
            log_path.mkdir(parents=True, exist_ok=True)
        return log_path
    
    @classmethod
    def get_log_filepath(cls):
        """Get the log file path."""
        return cls.get_log_dir(create=True) / LOG_FILE_NAME
    
    @classmethod
    def get_log_archive_filepath(cls):
        """Get the log archive file path."""
        return cls.get_log_dir(create=True) / LOG_FILE_NAME_ARCHIVE
    
    @classmethod
    def get_profiles_filepath(cls):
        """Get the profiles file path."""
        return cls.get_project_root() / PROFILES_FILE_NAME
    
    @classmethod
    def get_docs_dir(cls):
        """Get the documentation directory."""
        docs_dir = cls.get_package_path() / 'docs'
        return docs_dir
    
    @classmethod
    def get_templates_dir(cls):
        """Get the templates directory."""
        templates_dir = cls.get_package_path() / 'templates'
        return templates_dir


    @classmethod
    def get_valid_profiles_path(cls):
        """
        Try multiple profile locations in order of preference.
        Returns the first valid profile path or raises ConfigurationError if none are valid.
        """
        profile_locations = [
            (cls.outside_profiles_filepath, "secrets directory"),
            (cls.get_profiles_filepath(), "project root"),
        ]
        
        errors = []
        
        for path, location_name in profile_locations:
            if path is None or not path.exists():
                errors.append(f"No profiles.yml found in {location_name} ({path})")
                continue
                
            try:
                with open(path, 'r') as file:
                    yaml.safe_load(file)
                return path
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {location_name} ({path}): {str(e)}")
            except Exception as e:
                errors.append(f"Error accessing {location_name} ({path}): {str(e)}")
        
        error_msg = "No valid profiles.yml found in any location:\n" + "\n".join(f"- {err}" for err in errors)
        raise ConfigurationError(error_msg)

    @classmethod
    def _get_secrets_directory(cls):
        """Find the secrets directory across multiple possible locations."""
        possible_locations = [
            # Current working directory
            Path(os.getcwd()) / 'secrets',
            
            # User's home directory
            Path.home() / 'flexquery' / 'secrets',
            
            # One directory up from working directory
            Path(os.getcwd()).parent / 'secrets',
            
            # Environment variable (if set)
            Path(os.environ.get('FLEXQUERY_SECRETS_DIR', '')) if os.environ.get('FLEXQUERY_SECRETS_DIR') else None,
        ]
        
        # Filter out None values and check existence
        return next((str(path) for path in possible_locations 
                    if path and path.is_dir()), 
                    None)
    
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        paths = [cls.get_output_dir(), cls.get_queries_lib_dir(), cls.get_log_dir()]
        
        for path in paths:
            os.makedirs(path, exist_ok=True)
        
        return {
            'output': cls.get_output_dir(),
            'queries': cls.get_queries_lib_dir(),
            'logs': cls.get_log_dir()
        }
    

    @classmethod
    def initialize_class_vars(cls):
        """Initialize class variables that depend on methods."""
        cls.secrets_dir = cls._get_secrets_directory()
        cls.outside_profiles_filepath = Path(cls.secrets_dir) / PROFILES_FILE_NAME if cls.secrets_dir else None


AppPaths.initialize_class_vars()

