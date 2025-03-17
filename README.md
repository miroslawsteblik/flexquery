# FlexQuery
A flexible, parameter-driven SQL query execution tool that connects to multiple database environments.

# Overview
FlexQuery is a Python-based utility for efficiently running parameterized SQL queries against different database environments. It supports both DuckDB (for testing) and Microsoft SQL Server (for production data warehouse), with robust parameter handling, logging, and output formatting.

# Features
Database Environment Support:

- DuckDB for local testing
- Microsoft SQL Server for production data warehouse access

# Parameterized Queries:

- Dynamic parameter substitution in SQL queries
- Support for single values and lists in WHERE clauses
- Automatic handling of IN clauses with proper SQL syntax
# Robust Logging:

- Daily log rotation with archive capability
- Function execution tracking
- Comprehensive error handling
- User-Friendly Interface:

# Interactive SQL file selection
- Parameter validation
- Results preview and export

# Installation

## Clone project
```bash
git clone https://github.com/miroslawsteblik/flexquery.git
cd flex-query
```

## Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

## Install
```bash
pip install -e.  # for development mode
```


## Create `environment.yml` file with your database connections
### Example:
```yml
flexquery:
  outputs:
    TEST:
      type: duckdb
      path: '.\\testdatabase.db'

    DEV:
      type: mssql
      server: '<your_dev_server>'
      database: '<your_dev_database>'

    PROD:
      type: mssql
      server: '<your_prod_server>'
      database: '<your_prod_database>'
```

## Usage
### Run with specified environment
```bash
flexquery --env DEV  # For development database
flexquery --env UAT  # For user acceptance testing
flexquery --env PROD --write-csv # For production data warehouse and saving output
flexquery --env TEST  # For local DuckDB testing
```


## SQL Query Parameters
Parameters in SQL queries use the :parameter_name syntax:

```sql
-- Example query showing parameter usage
SELECT * FROM users
WHERE company_id = :company_id
  AND status IN :status_list
```

## Define parameters in `params.yml`
```yml
company_id: 123
status_list:
  - "active"
  - "pending"
```

# Database Support
- Test Environment: Uses DuckDB, a lightweight analytical database that runs locally without a server
- Production Environment: Connects to Microsoft SQL Server data warehouse

# Configuration
Environment-specific configuration is loaded from `environment.yml` file:

- Database servers
- Database names
- Connection parameters

# Example Output
FlexQuery can output results to:

- Console preview
- CSV files
- Other formats based on configuration