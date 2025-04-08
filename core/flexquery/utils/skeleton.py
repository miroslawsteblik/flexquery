import os
import shutil
import pkg_resources
from typing import Tuple, Optional
from flexquery.config.pathconfig import AppPaths



def initialize_env_directories(env: Optional[str] = None) -> None:
    """
    Create necessary directories if they don't exist.
    
    Args:
        env (str, optional): Environment name to create specific directories for. Defaults to None.
    """
    # Create main directories
    os.makedirs(AppPaths.get_output_dir(), exist_ok=True)
    os.makedirs(AppPaths.get_log_dir(), exist_ok=True)
    os.makedirs(AppPaths.get_queries_lib_dir(), exist_ok=True)
    
    # Create environment-specific output directory and queries library directory
    if env:
        os.makedirs(os.path.join(AppPaths.get_output_dir(), env), exist_ok=True)
        os.makedirs(os.path.join(AppPaths.get_queries_lib_dir(), env), exist_ok=True)


def find_template_file(template_name: str) -> Optional[str]:
    """Find the path to a template file."""
    try:
        template_path = pkg_resources.resource_filename("flexquery", os.path.join("docs", "templates", template_name))
        if os.path.exists(template_path):
            return template_path
        else:
            raise FileNotFoundError(f"file not found")
    except Exception as e:
        raise FileNotFoundError(f"Template file error: {template_name}. Details: {str(e)}")


def copy_template_file(template_name: str, destination_path: str, silent: bool = False) -> Tuple[bool, str]:
    """Copy a template file to the destination path"""
    # Don't overwrite existing file
    if os.path.exists(destination_path):
        return False
    
    # Find template file
    template_path = find_template_file(template_name)

    if not template_path:
        raise FileNotFoundError(f"file not found: {template_name}")
    
    try:
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        shutil.copy2(template_path, destination_path)
        return True
    except Exception as e:
        return False, f"Error copying template file: {e}"


def _create_template_file(template_name: str, path: str, file_type: str, silent: bool = False) -> Tuple[bool, str]:
    """Generic function to create a template file if it doesn't exist."""
    if os.path.exists(path):
        return False

    return copy_template_file(template_name, path, silent)


def create_profiles_template(path: Optional[str] = None, silent: bool = False) -> Tuple[bool, str]:
    """Create a template profiles.yml file if it doesn't exist"""
    if path is None:
        path = AppPaths.get_profiles_filepath()
    
    return _create_template_file("profiles_example.yml", path, "Profiles", silent)


def create_params_template(env: str, path: Optional[str] = None, silent: bool = False) -> Tuple[bool, str]:
    """Create a template params.yml file for the specified environment."""
    if path is None:
        path = os.path.join(AppPaths.get_queries_lib_dir(), env, 'params.yml')
    
    return _create_template_file("params_example.yml", path, "Parameters", silent)


def create_sql_template(env: str, path: Optional[str] = None, silent: bool = False) -> Tuple[bool, str]:
    """Create a template SQL query file for the specified environment"""
    if path is None:
        path = os.path.join(AppPaths.get_queries_lib_dir(), env, 'query.sql')
    
    return _create_template_file("query_example.sql", path, "Query", silent)






