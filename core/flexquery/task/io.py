from io import StringIO
import pandas as pd

from flexquery.utils.calculations import CommsCalculations

from flexquery.config.logging_config import log_execution, get_logger
logger = get_logger(__name__)

def capture_dataframe_info(df: pd.DataFrame) -> str:
    """ Capture and return the info() output for a DataFrame """
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return info_str

@log_execution    
def write_to_csv( df: pd.DataFrame, file_name: str, output_dir: str) -> str:
    """
    Save query results DataFrame to a CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        file_name (str): Base name for the output file (without extension)
        output_dir (str): Directory to save the file in
        query_file (str): Path to the original query file (for metadata)
    Returns:
        str: Full path to the saved CSV file, or None if no data was saved
    """
    if df is None or df.empty:
        logger.warning(f"No data to save for {file_name}")
        return None
    
    output_file = f"{output_dir}\{file_name}.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"\nData written to: {output_file}")
    
    return output_file

@log_execution
def write_to_excel(df: pd.DataFrame, file_name: str, output_dir: str) -> str:
    """
    Save query results DataFrame to an Excel file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        file_name (str): Base name for the output file (without extension)
        output_dir (str): Directory to save the file in
        query_file (str): Path to the original query file (for metadata)
    Returns:
        str: Full path to the saved Excel file, or None if no data was saved
    """

    if df is None or df.empty:
        logger.warning(f"No data to save for {file_name}")
        return None

    spc = CommsCalculations(df)

    output_file = f"{output_dir}\{file_name}.xlsx"
    spc.save_to_excel( output_file)
    logger.info(f"\nData written to: {output_file}")
    
    return output_file

def write_to_json(df: pd.DataFrame, file_name: str, output_dir: str) -> str:
    """
    Save query results DataFrame to a JSON file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        file_name (str): Base name for the output file (without extension)
        output_dir (str): Directory to save the file in
        query_file (str): Path to the original query file (for metadata)
    Returns:
        str: Full path to the saved JSON file, or None if no data was saved
    """
    if df is None or df.empty:
        logger.warning(f"No data to save for {file_name}")
        return None
    
    output_file = f"{output_dir}\{file_name}.json"
    df.to_json(output_file, orient='records', lines=True)
    logger.info(f"\nData written to: {output_file}")
    
    return output_file
