import os
from pathlib import Path
from flexquery.config.constants import (
    OUTPUT_DIR_NAME, ENVIRONMENT_FILE_NAME, QUERIES_LIBRARY_NAME, LOG_DIR_NAME, LOG_FILE_NAME
)

# Base directories
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Points to /flex-query
FLEXQUERY_DIR = os.path.join(BASE_DIR, 'core', 'flexquery')



# Path construction function
def get_path(*parts):
    """Construct a path from base directory and parts"""
    return os.path.join(BASE_DIR, *parts)

def get_flexquery_path(*parts):
    """Construct a path within the flexquery directory"""
    return os.path.join(FLEXQUERY_DIR, *parts)


# -------------------------- [ PATHS OUTPUTS ] ------------------------------------------------ #
OUTPUT_DIR = get_flexquery_path(OUTPUT_DIR_NAME)
ENVIRONMENT_PATH = get_path(ENVIRONMENT_FILE_NAME)
QUERIES_LIBRARY = get_flexquery_path(QUERIES_LIBRARY_NAME)
LOG_PATH = get_flexquery_path(LOG_DIR_NAME, LOG_FILE_NAME)
LOG_ARCHIVE_PATH = get_flexquery_path(LOG_DIR_NAME, f"{LOG_FILE_NAME}.archive")
# ------------------------------- [ END ]------------------------------------------------------- #


# Function to ensure directories exist
def ensure_app_directory(directory):
    """Create necessary directories if they don't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)