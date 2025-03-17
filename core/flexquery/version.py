import click

def version_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"flex-query version {__version__}")
    ctx.exit()

__version__ = '1.1.0'