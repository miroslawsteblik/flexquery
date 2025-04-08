import yaml

from flexquery.config.exceptions import ConfigurationError
from flexquery.config.pathconfig import AppPaths


class Config:
    def __init__(self, env, win_auth, **kwargs):
        self.env = env 
        self.envvar = self._load_profiles()['flexquery']['outputs'].get(env) 
        self.params = self._get_params(env)
        self.win_auth = win_auth
        self.username = self.envvar.get('username')
        self.password = self.envvar.get('password')
        self.db_type = self.envvar.get('type')
        self.db_path = self.envvar.get('path')
        self.server = self.envvar.get('server')
        self.database = self.envvar.get('database')
        self.application_intent = self.envvar.get('read_only')
        self.validate()

    
    def validate(self):
        if self.db_type not in ['duckdb', 'mssql']:
            raise ConfigurationError(f"Unsupported database type: {self.db_type}")
        if self.db_type == 'duckdb' and not self.db_path:
            raise ConfigurationError("DuckDB requires a valid db_path")
        if self.db_type == 'duckdb' and not self.db_path.endswith('.db'):
            raise ConfigurationError("Invalid database path specified in profiles.yml")
        if self.db_type == 'mssql' and not self.server:
            raise ConfigurationError("MSSQL requires a valid server")
        if not self.env:
            raise ConfigurationError("Environment is required for running SQL queries")
        if not self.envvar:
            raise ConfigurationError(f"Environment '{self.env}' not found in profiles.yml")


    def _load_profiles(self):
        try:
            profiles_path = AppPaths.get_valid_profiles_path()

            with open(profiles_path, 'r') as file:
                profile = yaml.safe_load(file)
            return profile

        except FileNotFoundError as e:
            raise ConfigurationError(profiles_path) from None
        except yaml.YAMLError as e:
            raise ConfigurationError(profiles_path) from None

    def _get_params(self, env=None):
        """Retrieve parameters from environment-specific params.yml file."""
        if not env:
            return {}
        
        # Construct path to the environment-specific params.yml file
        params_path = AppPaths.get_queries_lib_dir().joinpath(env, 'params.yml')

        try:
            if params_path.exists():
                with open(params_path, 'r') as file:
                    parameters = yaml.safe_load(file) or {}
                return parameters
            else:
                # No params file found, return empty dict
                return {}
        except FileNotFoundError as e:
            raise ConfigurationError(params_path) from None
        except yaml.YAMLError as e:
            raise ConfigurationError(params_path) from None




