import os
from io import StringIO
from typing import Optional
import pandas as pd

from flexquery.config.logging_config import log_execution, get_logger
logger = get_logger(__name__)

def _capture_dataframe_info(df: pd.DataFrame) -> str:
    """ Capture and return the info() output for a DataFrame """
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return info_str

@log_execution    
def save_data_to_csv( df: pd.DataFrame, file_name: str, output_dir: str) -> str:
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
        
    logger.info(f"DataFrame summary:\n{_capture_dataframe_info(df)}")
    
    # Save to CSV
    output_file = f"{output_dir}/{file_name}.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Data written to: {output_file}")
    
    return output_file