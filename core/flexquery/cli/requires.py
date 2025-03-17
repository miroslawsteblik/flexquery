import functools
import os
import click
from datetime import datetime

from flexquery.connection import SQLConnectionManager
from flexquery.processor import DataProcessor
from flexquery.config.config import Config
from flexquery.config.logging_config import get_logger, log_separator
from flexquery.config.pathconfig import QUERIES_LIBRARY, OUTPUT_DIR, ensure_app_directory
from flexquery.utils import save_data_to_csv, _capture_dataframe_info


logger = get_logger(__name__)

def with_config(func):
    """Decorator to inject config and parameters into a function."""
    @functools.wraps(func)
    def wrapper(env, *args, **kwargs):
        logger.debug(f"Loading configuration for {env} environment")
        log_separator(env=env)
        config = Config(env)
        return func(
            env=env,
            config=config,
            *args, 
            **kwargs
        )
    return wrapper

def with_connection_manager(func):
    """Decorator to inject only the database connection manager into a function."""
    @functools.wraps(func)
    def wrapper(env, config, *args, **kwargs):
        # Set up database connection
        logger.debug(f"Setting up connection manager for {env} environment")
        config = config
        connection_manager = SQLConnectionManager(config)
        return func(
            env=env, 
            config=config,
            connection_manager=connection_manager,
            *args, 
            **kwargs
        )
    return wrapper

def with_data_processor(func):
    """Decorator to inject a data processor into a function."""
    @functools.wraps(func)
    def wrapper(env, config, connection_manager, *args, **kwargs):
        # Create data processor using the provided connection manager
        logger.debug(f"Creating data processor for {env} environment")
        data_processor = DataProcessor(connection_manager.connection)
        return func(
            env=env,
            config=config,
            connection_manager=connection_manager, 
            data_processor=data_processor,
            *args, 
            **kwargs
        )
    return wrapper


def with_query_params(func):
    """Decorator to inject config and parameters into a function."""
    @functools.wraps(func)
    def wrapper(env, config, *args, **kwargs):
        # Set up configuration
        logger.debug(f"Loading configuration for {env} environment")
        config = config
        query_parameters = config.params
        return func(
            env=env,
            config=config,
            query_parameters=query_parameters,
            *args, 
            **kwargs
        )
    return wrapper

def with_sql_selection(func):
    """Decorator to handle SQL file selection from environment directory."""
    @functools.wraps(func)
    def wrapper(env, *args, **kwargs):
        env_dir = os.path.join(QUERIES_LIBRARY, env)
        
        sql_files = [f.replace('.sql', '') for f in os.listdir(env_dir) 
                    if f.endswith('.sql') and os.path.isfile(os.path.join(env_dir, f))]  
        if not sql_files:
            logger.error(f"No SQL query files found in {env_dir}")
            raise click.UsageError(f"No SQL files found in environment: {env}")
        
        print(f"\nAvailable queries for {env} environment:")
        for i, file in enumerate(sql_files, 1):
            print(f"{i}. {file}")
        
        selection = click.prompt("Select a query to run (number)", type=int, default=1)
        
        try:
            query_file = sql_files[selection - 1]
            logger.info(f"Selected query: {query_file}.sql")
        except IndexError:
            logger.error(f"Invalid selection: {selection}")
            raise click.UsageError(f"Selection must be between 1 and {len(sql_files)}")
        
        # Construct full path to query file
        query_path = os.path.join(QUERIES_LIBRARY, env, f"{query_file}.sql")
        if not os.path.exists(query_path):
            logger.error(f"Query file not found: {query_path}")
            raise click.FileError(query_path, hint="Make sure the file exists in the environment directory")
        
        # Print SQL file for reference
        with open(query_path, 'r') as file:
            logger.info(f"SQL query:\n{file.read()}")
            
        return func(
            env=env,
            query_file=query_file,
            query_path=query_path,
            *args,
            **kwargs
        )
    return wrapper

def output(func):
    """Decorator to handle saving query results to CSV."""
    @functools.wraps(func)
    def wrapper(env, query_file, *args, **kwargs):

        write_csv = kwargs.get('write_csv', False)

        df = func(env=env, query_file=query_file, *args, **kwargs)
        
        if df is not None and not df.empty:
            if write_csv:
                base_name = os.path.basename(query_file).replace('.sql', '')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = f"{env}_{base_name}_{timestamp}"
                ensure_app_directory(OUTPUT_DIR)
                output_file = save_data_to_csv(df, file_name, OUTPUT_DIR)
                return output_file
            else:
                logger.info(f"DataFrame summary:\n{_capture_dataframe_info(df)}")
                logger.info("Results displayed in console. Use --write-csv to save to file.")
                return df
        else:
            logger.info("Query returned no results")
            return None
    return wrapper