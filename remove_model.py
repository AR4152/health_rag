"""MLHub Toolkit for health_rag - remove_model.

Command-line tool to remove LLM models via Ollama.

Usage:
    ml remove_model health_rag <model_name>
"""

import argparse
import subprocess


def remove_model(model: str) -> None:
    """Remove a specified LLM model using the Ollama CLI.

    Args:
        model (str): The name of the model to remove.

    """
    try:
        print(f"Removing model: {model}\n")
        result = subprocess.run(["ollama", "rm", model], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error removing model:\n{e.stderr}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a LLM model using the Ollama CLI.")
    parser.add_argument(
        "model", type=str, help="The name of the model to remove (e.g., 'llama3.2:1b')."
    )
    args = parser.parse_args()

    remove_model(args.model)
