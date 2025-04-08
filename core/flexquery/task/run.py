from flexquery.task.base import Task
from flexquery.utils.connection import DuckDBConnectionManager, MSSQLWindowsAuthConnectionManager, MSSQLUsernamePasswordConnectionManager
from flexquery.utils.processor import FlexQuery
from flexquery.config.exceptions import ConfigurationError, DatabaseConnectionError, DataProcessorError
from flexquery.utils import skeleton
from flexquery.config.config import Config
from flexquery.task.io import write_to_csv, write_to_excel, write_to_json ,capture_dataframe_info
from flexquery.config.logging_config import get_logger
from flexquery.config.pathconfig import  AppPaths

import click
from pathlib import Path
from datetime import datetime


logger = get_logger(__name__)


class RunTask(Task):
    """Task for executing SQL queries."""

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._env = kwargs.get("env", None)
        self.write_csv = kwargs.get('write_csv', False)
        self.write_excel = kwargs.get('write_excel', False)
        self.write_json = kwargs.get('write_json', False)
        self.win_auth = kwargs.get('win_auth', False)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.config = Config(self._env, win_auth=self.win_auth, username=self.username, password=self.password)
        self.query_parameters = self.config.params
        self.env_dir = AppPaths.get_queries_lib_dir().joinpath(self._env)
        if self.config.db_type == "duckdb":
            self._connection_manager = DuckDBConnectionManager(self.config)
        elif self.config.db_type == "mssql" and self.config.win_auth:
            self._connection_manager = MSSQLWindowsAuthConnectionManager(self.config)
        elif self.config.db_type == "mssql":
            self._connection_manager = MSSQLUsernamePasswordConnectionManager(self.config)
        else:
            raise ConfigurationError(f"Unsupported database type: {self.config.db_type}")


    def validate(self):
        """Validate build requirements."""
        if not self._env:
            raise ConfigurationError("Environment is required for running SQL queries.")
        return True

    def setup(self):
        """Prepare for building."""
        logger.info(f"Executing SQL query for environment: {self._env}")
        skeleton.initialize_env_directories(self._env)
        self._connection_manager.create_engine()
        return True


    def _execute(self):
        """Execute the SQL query logic."""
        try:
            
            with self._connection_manager as conn:
                self._query_executor = FlexQuery(conn.connection, self.config)

                sql_files = self._get_sql_files(self.env_dir)
                if not sql_files:
                    raise ConfigurationError(f"No SQL files found in environment: {self.env_dir}")
                
                self._display_available_queries(sql_files, self._env)

                query_file = self._select_query(sql_files)
                query_path = self._get_query_path(self._env, query_file)

                if not query_path:
                    raise FileNotFoundError(f"Query file not found: {query_path}")
                self._log_query_content(query_path)

                result = self._query_executor.process_sql_query_with_params(query_path, self.query_parameters)

                if result is not None and not result.empty:
                    base_name = Path(query_file).stem
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    extract_params = '_'.join([str(v) for v in self.query_parameters.values()])
                    clean_params = extract_params.replace(' ', '_').replace("'", '').replace("[", '').replace("]", '').replace(",", '')
                    short_params = clean_params[:50] if len(clean_params) > 50 else clean_params
                    file_name = f"{base_name}_{short_params}_created_at_{timestamp}"
                    output_direnv = AppPaths.get_output_dir().joinpath(self._env)
                    summary = capture_dataframe_info(result)
                    logger.debug(f"Query results summary:\n{summary}")

                    if self.write_csv:
                            try:
                                csv_file = write_to_csv(result, file_name, output_direnv)
                            except DataProcessorError as e:
                                raise DataProcessorError(f"Error writing CSV file: {e}") from None

                    if self.write_excel:
                        try:
                            excel_file = write_to_excel(result, file_name, output_direnv)
                        except DataProcessorError as e:
                            raise DataProcessorError(f"Error writing Excel file {e}") from None
                        
                    if self.write_json:
                        try:
                            json_file = write_to_json(result, file_name, output_direnv)
                        except DataProcessorError as e:
                            raise DataProcessorError(f"Error writing JSON file {e}") from None
                else:
                    logger.warning("No results returned from the SQL query.")
                    return False        
                if not self.write_csv and not self.write_excel and not self.write_json:
                    logger.warning("Results displayed in log file only. Use --write-csv or --write-excel to save to save your results.")
                return True
            
        except DatabaseConnectionError as e:
            raise DatabaseConnectionError(f"Workflow failed due to database connection issue: {e}")
        except DataProcessorError as e:
            raise DataProcessorError(f"Workflow failed during data processing: {e}")
        except Exception as e:
            raise Exception(f"Workflow failed due to: {e}") from None
        
        
    def cleanup(self):
        pass
        

    def _get_sql_files(self, env_dir):
        """Get the list of SQL files in the environment directory."""
        sql_files = [entry.name.replace('.sql', '') for entry in env_dir.iterdir()
                    if entry.is_file() and entry.name.endswith('.sql')]
        if not sql_files:
            raise ConfigurationError(f"No SQL files found in environment: {env_dir}")
        return sql_files

    def _display_available_queries(self, sql_files, env):
        print(f"\nAvailable queries for {env} environment:")
        for i, file in enumerate(sql_files, 1):
            print(f"{i}. {file}")

    def _select_query(self, sql_files):
        selection = None
        while selection not in range(1, len(sql_files) + 1):
            selection = click.prompt("Select a query to run (number)", type=int)
            if selection not in range(1, len(sql_files) + 1):
                logger.error(f"Invalid selection. Selection must be between 1 and {len(sql_files)}")
        query_file = sql_files[selection - 1]
        logger.info(f"Selected query: {query_file}.sql")
        return query_file

    def _get_query_path(self, env, query_file):
        query_path = AppPaths.get_queries_lib_dir().joinpath(env, f"{query_file}.sql")
        if not query_path.exists():
            raise FileNotFoundError(f"Query file not found: {query_path}")
        return query_path

    def _log_query_content(self, query_path):
        with open(query_path, 'r') as file:
            logger.debug(f"SQL query:\n{file.read()}")