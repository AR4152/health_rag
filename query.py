# MLHub toolkit for health_rag - query
# ml query health_rag

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import click
from langchain_ollama import ChatOllama

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("query", required=True)

def cli(query: str):
    """
    Simple `hello world` string output.
    """
    
    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0.8,
        num_predict=256,
    )

    messages = [
        ("human", query),
    ]

    ai_msg = llm.invoke(messages)
    print(ai_msg.content)

if __name__ == "__main__":
    cli(prog_name="query")