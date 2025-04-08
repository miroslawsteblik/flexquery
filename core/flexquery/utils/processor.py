import pandas as pd
from typing import Optional
from sqlalchemy import text, bindparam
import re

from flexquery.config.exceptions import SQLQueryError

from flexquery.config.logging_config import log_execution, get_logger
logger = get_logger(__name__)

    

class QueryExecutor:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query: str, parameters: dict) -> Optional[pd.DataFrame]:
        """ Execute a SQL query from a file with parameters from user_parameters."""
        try:
            query = text(query).bindparams(**parameters)
            return pd.read_sql(query, self.connection)
        except Exception as e:
            raise SQLQueryError(f"Error executing query: {e}") from None
    

class QueryProcessor:
    @staticmethod
    @log_execution
    def extract_parameters_from_sql(sql_content: str) -> list:
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
    
    @staticmethod
    def validate_parameters(params_dict: dict):
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


class FlexQuery:
    def __init__(self, connection, config):
        self._query_executor = QueryExecutor(connection)
        self.config = config

    def process_sql_query_with_params(self, query_file: str, user_parameters: dict) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query from a file with parameters from user_parameters.
        Args:
            query_file (str): The path to the file containing the SQL query.
            user_parameters (dict): user_parameters dictionary containing parameter values.
        Returns:
            pd.DataFrame: A DataFrame containing the query results if successful, None otherwise.
        """
            
        with open(query_file, 'r') as file:
            query_str = file.read()
            
        required_params = QueryProcessor.extract_parameters_from_sql(query_str)
        logger.debug(f"Required parameters: {required_params}")

        default_params = self.config.params or {}
        merged_params = {**default_params, **(user_parameters or {})}
        final_params = {k: merged_params.get(k) for k in required_params if k in merged_params}

        missing_params = [p for p in required_params if p not in final_params]
        if missing_params:
            raise SQLQueryError(f"Missing required parameters: {missing_params}")

        QueryProcessor.validate_parameters(user_parameters)
            
        modified_query = query_str

        bind_params = []
        for param in required_params:
            if param in user_parameters:
                pattern = re.compile(fr"(in|IN)\s+:{param}\b", re.IGNORECASE) # Match IN :param

                param_value = user_parameters[param]
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

        return self._query_executor.execute_query(modified_query, {param.key: param.value for param in bind_params})
                        


        
