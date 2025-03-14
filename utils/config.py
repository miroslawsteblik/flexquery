import dotenv
import yaml
import sys

class Config:
    def __init__(self, env):
        self.env = env
        if env =='TEST':
            self.db_type = 'duckdb'
            self.db_path = dotenv.get_key('.env', "DUCKDB_PATH")
        else:
            self.db_type = 'mssql'
            self.server = dotenv.get_key('.env', f"{env}_DB_SERVER")
            self.database = dotenv.get_key('.env', f"{env}_DB_DATABASE")

def get_config(env):
    return Config(env)

def get_params(file_path='flexquery/utils/params.yml'):
    try:
        with open(file_path, 'r') as file:
            parameters = yaml.safe_load(file)
        return parameters
    except Exception as e:
        print(f"Error reading parameters file: {e}")
        sys.exit(1)


