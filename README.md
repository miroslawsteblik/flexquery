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
## Clone the repository
`git clone https://github.com/miroslawsteblik/flexquery.git`
`cd FlexQuery`

## Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

## Install dependencies
`pip install -r requirements.txt`

## Create .env file with your database connections
### Example:
```yml
DEV_DB_SERVER=your_dev_server
DEV_DB_DATABASE=your_dev_database
UAT_DB_SERVER=your_uat_server
UAT_DB_DATABASE=your_uat_database
PROD_DB_SERVER=your_prod_server
PROD_DB_DATABASE=your_prod_database
DUCKDB_PATH=path/to/your/test.db
```

## Usage
### Run with specified environment
```bash
python -m flexquery --env DEV  # For development database
python -m flexquery --env UAT  # For user acceptance testing
python -m flexquery --env PROD  # For production data warehouse
python -m flexquery --env TEST  # For local DuckDB testing
```

## Architecture
FlexQuery consists of:

- Connection Manager: Handles database connections for different environments
- Data Processor: Processes SQL queries with parameter substitution
- Parameter Handling: Validates and transforms parameters for SQL execution
- Logging System: Maintains daily logs and archives

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
Environment-specific configuration is loaded from .env file:

- Database servers
- Database names
- Connection parameters

# Example Output
FlexQuery can output results to:

- Console preview
- CSV files
- Other formats based on configuration