import pandas as pd
from typing import Optional
from sqlalchemy import text, bindparam
from flexquery.utils.logging_config import log_execution, get_logger
import re
import os
from io import StringIO


logger = get_logger(__name__)

        
class DataProcessor:
    def __init__(self, connection, valid_tables=None):
        self.connection = connection
        self.valid_tables = valid_tables or []

    @staticmethod
    @log_execution
    def extract_parameters_from_sql(sql_content):
        """
        Extract parameter names from SQL content by looking for :parameter_name patterns.
        Args:
            sql_content (str): The SQL query content
        Returns:
            list: List of parameter names found in the SQL
        """
        param_pattern = re.compile(r':([a-zA-Z0-9_]+)')
        params = param_pattern.findall(sql_content)
        return list(set(params))  

    @log_execution
    def execute_query(self, query_file: str, query_parameters: dict) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query from a file with parameters from query_parameters.
        Args:
            query_file (str): The path to the file containing the SQL query.
            query_parameters (dict): query_parameters dictionary containing parameter values.
        Returns:
            pd.DataFrame: A DataFrame containing the query results if successful, None otherwise.
        """
        if not self.connection:
            logger.error("No connection available")
            return None
            
        with open(query_file, 'r') as file:
            query_str = file.read()
            
        try:
            required_params = self.extract_parameters_from_sql(query_str)
            logger.info(f"Required parameters: {required_params}")
            self.validate_parameters(query_parameters)
            modified_query = query_str

            bind_params = []
            for param in required_params:
                if param in query_parameters:
                    pattern = re.compile(fr"(in|IN)\s+:{param}\b", re.IGNORECASE) # Match IN :param

                    param_value = query_parameters[param]
                    if isinstance(param_value, list) and len(param_value) > 1:
                        placeholder_list = []
                        for i, item in enumerate(param_value):
                            bind_name = f"{param}_{i}"
                            placeholder_list.append(f":{bind_name}")
                            bind_params.append(bindparam(bind_name, item))
                        
                        # Replace :param with (:param_0, :param_1, ...)
                        placeholder_str = f"({', '.join(placeholder_list)})"
                        
                        # Replace the parameter in the query with the placeholder list
                        modified_query = pattern.sub(f"IN {placeholder_str}", modified_query)
                    else:
                        if isinstance(param_value, list) and len(param_value) == 1:
                            param_value = param_value[0]  # Extract the single value from the list
                        bind_params.append(bindparam(param, param_value))
                        if pattern.search(modified_query):
                            modified_query = pattern.sub(f"= :{param}", modified_query) # Replace IN :param with = :param for single values

            
            logger.info(f"Executing query with parameters: {bind_params}")

            query = text(modified_query)
            if bind_params:
                query = query.bindparams(*bind_params)
            
            df = pd.read_sql(query, self.connection)
            if df.empty:
                logger.info("\nQuery returned no data")
            return df
            
        except Exception as e:
            logger.error(f"\nError executing query: {e}")
            return None
    
    @log_execution
    def validate_parameters(self, params_dict):
        """
        Validate the types and values of parameters in a dictionary.

        This method checks if the values in the provided dictionary conform to
        the allowed types: int, str, float, list, bool, or NoneType. If a value
        is a list, it further validates that all items in the list are of the
        allowed types.

        Args:
            params_dict (dict): A dictionary where keys are parameter names and
                values are the parameters to validate.

        Raises:
            ValueError: If a parameter value or a list item has an invalid type.
        """
        for key, value in params_dict.items():
            if not isinstance(value, (int, str, float, list, bool, type(None))):
                raise ValueError(f"Invalid parameter type for {key}: {type(value)}")
            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, (int, str, float, bool, type(None))):
                        raise ValueError(f"Invalid list item type in {key}: {type(item)}")
        
    @log_execution    
    def save_data_to_csv(self, df: pd.DataFrame, file_name: str, output_dir: str) -> str:
        """
        Save query results DataFrame to a CSV file.
        
        Args:
            df (pd.DataFrame): DataFrame to save
            file_name (str): Base name for the output file (without extension)
            output_dir (str): Directory to save the file in
            query_file (str): Path to the original query file (for metadata)
            env (str): Environment identifier (for logging and filename)
            
        Returns:
            str: Full path to the saved CSV file, or None if no data was saved
        """
        if df is None or df.empty:
            logger.warning(f"No data to save for {file_name}")
            return None
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        
        # Capture and log DataFrame information
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        logger.info(f"DataFrame summary:\n{info_str}")
        
        # Save to CSV
        output_file = f"{output_dir}/{file_name}.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Data written to: {output_file}")
        
        return output_file


