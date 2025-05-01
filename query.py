# MLHub toolkit for health_rag - query
# ml query health_rag

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import click

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("query", required=True)

def cli(query: str):
    """
    Simple `hello world` string output.
    """

    print("Hello world!")

if __name__ == "__main__":
    cli(prog_name="query")