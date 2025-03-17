# FlexQuery Package
This package provides a flexible, parameter-driven SQL query execution tool that connects to multiple database environments.

# Overview
FlexQuery allows data analysts, engineers and developers to:

1. Run SQL queries against multiple environments (DEV, UAT, PROD, TEST)
2. Use parameter-driven queries with environment-specific configurations
3. Output results to console or CSV files
4. Manage database connections consistently

## Instalation
### Option 1: Install from Local Package
1. Build wheel package locally:
```bash
python -m build
```
2. Copy wheel to server (from your dist/ directory)
3. Install on server:
```bash
pip install flexquery-<version>-py3-none-any.whl
```

### Option 2: Install in Development Mode
1. Copy project to directory
2. Go to root directory and install in editable mode
```bash 
cd flex-query
pip install -e .
```

## Directory Structure
```bash
flexquery/
├── cli/
│   ├── main.py        # CLI entry points
│   ├── params.py      # Parameter definitions
│   └── requires.py    # Decorator functions
├── config/
│   ├── config.py      # Configuration loader
│   ├── logging_config.py  # Logging setup
│   └── pathconfig.py  # Directory/file paths
├── connection/
│   └── __init__.py    # Database connection management
├── processor/
│   └── __init__.py    # Query processing and execution
├── queries_library/   # SQL query files organized by environment
│   ├── DEV/
│   ├── TEST/
│   ├── UAT/
│   └── PROD/
└── utils.py           # Utility functions
```


## Components
### Connection Manager
Handles database connections for different environments. Connection details are loaded from environment.yml file.

### Query Processor
Executes SQL queries with parameters and returns results as Pandas DataFrames.

### CLI Module
Provides command-line interface with modular decorators pattern:

- `with_config`: Loads environment configuration
- `with_query_params`: Loads query parameters
- `with_connection_manager`: Sets up database connection
- `with_data_processor`: Creates data processor for query execution
- `with_sql_selection`: Handles query file selection
- `output`: Manages result output (console/CSV)

## Developer Guide
### Adding a New Environment
1. Add connection details to environment.yml
2. Create directory in `queries_library/<ENV_NAME>/`
3. Add params.yml in the new environment directory

### Adding a New Query
1. Create .sql file in appropriate environment directory
2. Add any parameters in the format {{parameter_name}}
3. Update environment's `params.yml` if needed

### Adding a New CLI Command
```python
@cli.command("new_command")
@p.environment
@requires.with_config
# Add other required decorators
def new_command(env, config, **kwargs):
    """Command description."""
    # Implementation
```

## Testing Queries
Use the TEST environment which connects to DuckDB for quick testing:
```bash
flexquery query --env TEST
```
## Usage Examples
Interactive query selection:
```bash
flexquery query --env DEV
```
Save results to CSV
```bash
flexquery query --env PROD --write-csv
```
## Decorator Chain Order
When using multiple decorators, order matters! The proper order is:

- Output decorators (last to execute)
- SQL selection decorators
- Data processor decorators
- Connection decorators
- Parameter decorators
- Config decorators (first to execute)