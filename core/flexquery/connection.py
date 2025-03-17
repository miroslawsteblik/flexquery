from sqlalchemy import create_engine
from flexquery.config.logging_config import log_execution, get_logger
import pyodbc


logger = get_logger(__name__)


class SQLConnectionManager:
    def __init__(self, config):
        self.config = config
        self.engine = self.create_sqlalchemy_engine()
        self.connection = self.connect()

    @log_execution
    def create_sqlalchemy_engine(self):
        """Create a SQLAlchemy engine based on configuration."""

        # duckdb
        if self.config.db_type == 'duckdb':
            connection_string = f"duckdb:///{self.config.db_path}"
            return create_engine(connection_string)
        
        # mssql
        else:  
            connection_string = (
                f"mssql+pyodbc://@{self.config.server}/{self.config.database}?"
                f"driver=ODBC+Driver+17+for+SQL+Server&"
                f"trusted_connection=yes&"
                f"TrustServerCertificate=yes&"  # Handle SSL/TLS issues
                f"timeout=30&"                  # Connection timeout
                f"connect_timeout=30"           # Login timeout
            )
            
            try:
                logger.info(f"Testing direct ODBC connection to {self.config.server}...")
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    F"SERVER={self.config.server};"
                    f"DATABASE={self.config.database};"
                    f"Trusted_Connection=yes;"
                )
                test_conn = pyodbc.connect(conn_str, timeout=5)
                test_conn.close()
                logger.info("Direct ODBC connection successful!")
            except Exception as e:
                logger.info(f"Direct ODBC connection failed: {e}")
            
            return create_engine(
                connection_string,
                connect_args={"connect_timeout": 30},
                pool_pre_ping=True,   # Test connections before using
                pool_recycle=3600     # Recycle connections hourly
            )

    def connect(self):
        """Create a connection to the database."""
        try:
            connection = self.engine.connect()
            return connection
        except Exception as e:
            logger.error(f"\nError connecting to database: {e}")
            return None






