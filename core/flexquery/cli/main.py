import click
import functools

from flexquery.cli import requires
from flexquery.cli import params as p
from flexquery.config.logging_config import  get_logger

logger = get_logger(__name__)

def global_flags(func):
    @p.version
    @p.write_csv
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

# CLI
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@p.environment
@global_flags
def cli(**kwargs):
    """A flexible, parameter-driven SQL query execution tool that connects to multiple database environments."""


@cli.command("query")
@global_flags
@p.environment
@requires.with_config   
@requires.with_query_params
@requires.with_connection_manager
@requires.with_data_processor
@requires.with_sql_selection
@requires.output
def query(
        env, 
        config,
        connection_manager,
        data_processor,
        query_parameters,
        query_file,
        query_path,
        **kwargs
    ):
    return data_processor.execute_query(query_path,query_parameters)

            
if __name__ == "__main__":
    cli()


# flexquery [COMMANDS] [ENVIRONMENT] [OPTIONS]
# flexquery query -e DEV -w
