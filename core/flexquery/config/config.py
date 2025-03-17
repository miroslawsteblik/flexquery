import yaml
import sys
import os

from flexquery.config.pathconfig import ENVIRONMENT_PATH, QUERIES_LIBRARY


class Config:
    def __init__(self, env):
        self.envvar = get_environment()['flexquery']['outputs'].get(env)
        self.params = get_params(env)
        
        if not self.envvar:
            print(f"Error: Environment '{env}' not found in profile.yml")
            sys.exit(1)
            
        self.db_type = self.envvar['type']
        
        if self.db_type == 'duckdb':
            self.db_path = self.envvar['path']
        elif self.db_type == 'mssql':
            self.server = self.envvar['server']
            self.database = self.envvar['database']

def get_config(env):
    return Config(env)

        
def get_environment():
    try:
        with open(ENVIRONMENT_PATH, 'r') as file:
            profile = yaml.safe_load(file)
        return profile
    except Exception as e:
        print(f"Error reading profile file: {e}")
        sys.exit(1)

def get_params(env=None):
    """
    Retrieve parameters from environment-specific params.yml file.
    
    Args:
        env (str): Environment name (DEV, TEST, UAT, PROD)
        
    Returns:
        dict: Parameters from the params.yml file
    """
    if not env:
        return {}
    
    # Construct path to the environment-specific params.yml file
    params_path = os.path.join(QUERIES_LIBRARY, env, 'params.yml')
    try:
        if os.path.exists(params_path):
            with open(params_path, 'r') as file:
                parameters = yaml.safe_load(file) or {}
            return parameters
        else:
            # No params file found, return empty dict
            return {}
    except Exception as e:
        print(f"Error reading parameters file: {e}")
        return {}



