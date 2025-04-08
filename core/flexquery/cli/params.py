import click


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
    "-csv",
    is_flag=True,
    help="Write the query results to a CSV file"
)
write_excel = click.option(
    "--write-excel",
    "-xl",
    is_flag=True,
    help="Write the query results to an Excel file"
)

write_json = click.option(
    "--write-json",
    "-json",
    is_flag=True,
    help="Write the query results to a JSON file"
)

win_auth = click.option(
    "--win-auth", 
    is_flag=True,
    help="Use Windows authentication instead of SQL Server authentication"
)

username = click.option(
    "--username",
    "-u",
    default=None,
    help="SQL Server username (when using SQL authentication)",
    hidden=True
)

password = click.option(
    "--password",
    "-p",
    default=None,
    help="SQL Server password (when using SQL authentication)",
    hide_input=True,
    hidden=True
)


# currently not in use
interactive = click.option(
        "--interactive", "-i",
        is_flag=True,
        help="Start an interactive SQL query session."
    )

# docs_serve = click.option(
#     "--browser",
#     "-b",
#     is_flag=True,
#     help="Open the query results in a web browser."
# )