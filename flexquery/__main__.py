from flexquery import SQLConnectionManager, DataProcessor
from flexquery import get_config, get_params
from flexquery.utils.logging_config import log_separator, get_logger
import argparse
import sys
import os
from datetime import datetime

logger = get_logger(__name__)


query_dir = 'flexquery/queries'
output_dir = 'flexquery/output'


def parse_arguments():
    parser = argparse.ArgumentParser(description="Database Validator", prog="flexquery")
    parser.add_argument('--env', type=str, choices=['DEV', 'UAT', 'PROD', 'TEST'], required=True, help='Environment (DEV, UAT, PROD, TEST for DuckDB)')
    if len(sys.argv) == 1:
        print("No arguments provided. Use --help for more information.")
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def list_sql_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.sql')]

def select_sql_file(sql_files):
    print("Available SQL files:")
    for i, file in enumerate(sql_files, 1):
        print(f"{i}. {file}")

    choice = int(input("Select the SQL file to execute (enter the number): "))
    logger.info(f"Selected file: {sql_files[choice - 1]}")
    if choice < 1 or choice > len(sql_files):
        print("Invalid choice")
        sys.exit(1)

    return sql_files[choice - 1]


def main():
    args = parse_arguments()
    env = args.env 
    config = get_config(env)
    query_parameters = get_params()

    log_separator(env=env)
    
    connection_manager = SQLConnectionManager(config)
    data_processor = DataProcessor(connection_manager.connection) 

    sql_files = list_sql_files(query_dir)

    choice = select_sql_file(sql_files)
    query_file = os.path.join(query_dir, choice)

    # Print SQL file content for reference
    with open(query_file, 'r') as file:
        logger.info(f"SQL query:\n{file.read()}")


    df = data_processor.execute_query(query_file,query_parameters)
    if df is not None and not df.empty:
        base_name = os.path.basename(query_file).replace('.sql', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{env}_{base_name}_{timestamp}"
        output_file = data_processor.save_data_to_csv(df, file_name, output_dir)


if __name__ == "__main__":
    main()

# python -m flexquery --env DEV 
