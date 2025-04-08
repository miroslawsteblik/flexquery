import click
import functools
import sys

from flexquery.cli import params as p
from flexquery.version import __version__
from flexquery.config.exceptions import  ApplicationError
from flexquery.task.docs_serve import DocsServeTask
from flexquery.task.init import InitTask
from flexquery.task.run import RunTask

from flexquery.config.logging_config import get_logger
logger = get_logger(__name__)


def cli_error_handler(func):
    """Decorator to handle errors in CLI commands with user-friendly messages."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApplicationError as e:
            # These are expected errors with user-friendly messages already logged
            # Just exit with error code without showing traceback
            logger.error(f"FlexQuery Error: {e}")
            sys.exit(1)
        except Exception as e:
            # Unexpected errors - show message but conditionally show traceback
            logger.error(f"{str(e)}")
            sys.exit(1)
    return wrapper

def global_flags(func):
    @p.win_auth
    @p.username
    @p.password
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def output_flags(func):
    @p.write_json
    @p.write_csv
    @p.write_excel
    @p.interactive
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# Main CLI
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.version_option(version=__version__, prog_name="flexquery")  
@global_flags
@output_flags
@p.environment
def cli(**kwargs):
    """A flexible, parameter-driven SQL query execution tool that connects to multiple database environments"""
    pass


# run
@cli.command("run")
@p.environment
@global_flags
@output_flags
@cli_error_handler
def run(**kwargs):
    """Execute a SQL query"""

    task = RunTask(**kwargs)
    results = task.execute()
    return results


# init
@cli.command("init")
@p.environment
@cli_error_handler
def init(**kwargs):
    """Initialize FlexQuery configuration and project structure"""
    
    task = InitTask(**kwargs)
    return task.execute()


# docs
@cli.command("docs")
@cli_error_handler
def docs(**kwargs):
    """Show FlexQuery documentation."""

    task = DocsServeTask()
    return task.execute()


            
if __name__ == "__main__":
    cli()


