import pyodbc
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from flexquery.config.exceptions import DatabaseConnectionError

from flexquery.config.logging_config import  get_logger
logger = get_logger(__name__)

class BaseConnectionManager:
    def __init__(self, config):
        self.config = config

    def connect(self):
        """Create and return a connection to the database using the engine."""
        logger.info(f"Connecting to {self.config.db_type} database...")
        try:
            self.connection = self.engine.connect()
            logger.info("Database connection established successfully")
            return self.connection
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection failed: {e}") from e

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.debug("Database connection closed")
            self.connection = None
        if self.engine:
            self.engine.dispose()
            logger.debug("Database engine disposed")
            self.engine = None

    def validate_connection(self):
        """Validate that an existing connection is still working."""
        try:
            self.connection.execute(text("SELECT 1"))
            logger.debug("Connection validation successful")
            return True
        except Exception as e:
            logger.error(f"Connection validation failed: {e}")
            return False
        
    def __enter__(self):
        """Context manager entry point."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close()
        return False  # Do not suppress exceptions


class DuckDBConnectionManager(BaseConnectionManager):
    def create_engine(self):
        """Create a SQLAlchemy engine for DuckDB."""
        try:
            connection_string = f"duckdb:///{self.config.db_path}"
            self.engine = create_engine(connection_string, pool_pre_ping=True)
            logger.info("DuckDB engine created successfully")
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create DuckDB engine: {e}")
        

class MSSQLConnectionManager(BaseConnectionManager):
    def _application_intent(self):
        """Return the application intent (ReadOnly or ReadWrite)."""
        return self.config.application_intent or "ReadOnly"

    def test_connection(self, conn_str):
        """Test the MSSQL connection."""
        try:
            test_conn = pyodbc.connect(conn_str, timeout=5)
            test_conn.close()
            logger.info("MSSQL connection test successful")
        except Exception as e:
            raise DatabaseConnectionError(f"MSSQL connection test failed: {e}")
        

class MSSQLWindowsAuthConnectionManager(MSSQLConnectionManager):
    def create_engine(self):
        """Create a SQLAlchemy engine for MSSQL with Windows Authentication."""
        try:
            connection_string = (
                f"mssql+pyodbc://@{self.config.server}/{self.config.database}?"
                f"driver=SQL+Server&"
                f"trusted_connection=yes&"
                f"TrustServerCertificate=yes&"
                f"ApplicationIntent={self._application_intent()}&"
                f"connect_timeout=30&"
                f"timeout=30"
            )
            self.test_connection(
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.config.server};"
                f"DATABASE={self.config.database};"
                f"Trusted_Connection=yes;"
                f"ApplicationIntent={self._application_intent()};"
            )
            self.engine = create_engine(connection_string, pool_pre_ping=True)
            logger.info("MSSQL engine with Windows Authentication created successfully")
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create MSSQL engine: {e}")
        
class MSSQLUsernamePasswordConnectionManager(MSSQLConnectionManager):
    def create_engine(self):
        """Create a SQLAlchemy engine for MSSQL with username/password authentication."""
        try:
            username_encoded = quote_plus(self.config.username)
            password_encoded = quote_plus(self.config.password)
            connection_string = (
                f"mssql+pyodbc://{username_encoded}:{password_encoded}@"
                f"{self.config.server}/{self.config.database}?"
                f"driver=SQL+Server&"
                f"trusted_connection=no&"
                f"TrustServerCertificate=yes&"
                f"ApplicationIntent={self._application_intent()}&"
                f"connect_timeout=30&"
                f"timeout=30"
            )
            self.test_connection(
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.config.server};"
                f"DATABASE={self.config.database};"
                f"UID={self.config.username};"
                f"PWD={self.config.password};"
                f"ApplicationIntent={self._application_intent()};"
            )
            self.engine = create_engine(connection_string, pool_pre_ping=True)
            logger.info("MSSQL engine with username/password created successfully")
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create MSSQL engine: {e}")






