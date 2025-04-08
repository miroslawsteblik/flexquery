# FlexQuery

A flexible, parameter-driven SQL query execution tool that connects to multiple database environments.

## Overview

FlexQuery is a Python-based utility designed for efficiently executing parameterized SQL queries across different database environments. It bridges the gap between development and production by supporting both lightweight local databases and enterprise SQL servers.

## Features

### Database Support
- **DuckDB** for local testing without server dependencies
- **Microsoft SQL Server** for production data warehouse access

### Query Management
- Dynamic parameter substitution in SQL queries
- Support for single values and lists in WHERE clauses
- Automatic handling of IN clauses with proper SQL syntax

### User Experience
- Interactive SQL file selection
- Parameter validation
- Results preview and export options
- Consistent output formatting

### Robust Logging
- Daily log rotation with archive capability
- Function execution tracking
- Comprehensive error handling

## Installation

### Prerequisites
- Python 3.9+
- Pip package manager

### Navigate to your directory and create project root directory
```bash 
# Example
cd /d "D:\Programs"  
mkdir "D:\Programs\flex-query"  
cd "D:\Programs\flex-query"
```

### Place the installation package in the root
`flex_query-<version>-py3-none-any.whl`

### Setup Virtual Environment
```bash
"D:\Programs\Python\Python311\python.exe" -m venv .venv
# For Windows
.venv\Scripts\activate 
# for bash
source .venv/bin/activate
```

### Install Package
```bash
# confirm if python and pip is available
python --version
pip --version
# install
pip install flex_query-<version>-py3-none-any.whl
```

### Finalization
- remove the installation package file

## Configuration 

### Initialization

```bash
# confirm if flexquery is installed
flexquery --version
# initialize 
flexquery init
```

### Database Connections
#### Create a `profiles.yml` file in either
- Your project root directory, or
- The `secrets/` directory one level above your project root

```yml
flexquery:
  outputs:
    TEST:
      type: duckdb
      path: ./testdatabase.db

    DEV:
      type: mssql
      server: <your_dev_server>
      database: <your_dev_database>

    PROD:
      type: mssql
      server: <your_prod_server>
      database: <your_prod_database>
```

### Query Parameters
Create a `params.yml` file in environment directory to define query parameters

```yml
company_id: 123
status_list:
  - active
  - pending
```

### SQL Query Syntax
Create sql query file in environment directory. Parameters in SQL queries use the `:parameter_name` syntax

```sql
-- Example query showing parameter usage
SELECT * FROM users
WHERE company_id = :company_id
  AND status IN :status_list
```

## Usage

### Basic Command Syntax

```bash
flexquery [OPTIONS] COMMAND [ARGS]
```

### Environment Options
```bash
flexquery run --env DEV    # Development database
flexquery run --env UAT    # User acceptance testing
flexquery run --env PROD   # Production data warehouse
flexquery run --env TEST   # Local DuckDB testing
```

### Output Options

#### With `--write-csv flag` - saves full query output to csv

```bash
flexquery --env DEV --write-csv      
```

#### With `--write-excel` flag - saves excel file with 4 tabs

- All
- Policy holders with no email
- Policy holders with no email and postcode
- Policy holders with no email and no postcode

```bash
flexquery run --env PROD --write-excel   
```

### Command Reference

FlexQuery provides several commands for different functionality:

#### `query` Command
Execute SQL queries from files or interactive input:

```bash
# test a query with in-memory database
flexquery run

# Run a query with windows authentication
flexquery run --env DEV --win-auth

# Run an interactive query session 
flexquery run --env PROD --interactive # in development
```

#### `docs` Command
Access documentation and examples:

```bash
# Open documentation in browser
flexquery docs 
```

#### `init` Command
Initialize a new FlexQuery project structure:

```bash
# Create basic project structure in current directory
flexquery init

flexquery init --env PROD
```


## Examples

### Complete Workflow Example

#### Create an SQL file `users_report.sql`

```sql
SELECT user_id, username, email, status
FROM users
WHERE department_id = :dept_id
  AND status IN :status_list
```

#### Define parameters in `params.yml`

```yml
dept_id: 42
status_list:
  - active
  - pending
```

#### Execute the query

```bash
flexquery --env DEV --sql users_report.sql --write-csv
```

## Output Options

- Console preview (default)
- CSV files (with `--write-csv`)
- Excel files (with `--write-excel`)
- JSON format (with `--write-json`) 

