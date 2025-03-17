import click
from flexquery.version import version_callback

environment = click.option(
    "--env",
    "-e",
    type=str,
    default="TEST",
    help="Which environment to use (DEV, UAT, PROD, TEST for DuckDB)",
    show_default=True
)

write_csv = click.option(
    "--write-csv",
    "-w",
    is_flag=True,
    help="Write the query results to a CSV file"
)

version = click.option(
    "--version",
    "-V",
    "-v",
    is_flag=True,
    callback = version_callback,
    help="Show version information and exit"
)