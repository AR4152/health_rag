"""MLHub Toolkit for health_rag - pull_model.

Command-line tool to pull LLM models via Ollama.

Usage:
    ml pull_model health_rag <model_name>
"""

import argparse
import subprocess


def pull_model(model: str) -> None:
    """Pull a specified LLM model using the Ollama CLI.

    Args:
        model (str): The name of the model to pull.

    """
    try:
        print(f"Pulling model: {model}\n")
        result = subprocess.run(
            ["ollama", "pull", model], capture_output=True, text=True, check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling model:\n{e.stderr}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull a LLM model using the Ollama CLI.")
    parser.add_argument(
        "model", type=str, help="The name of the model to pull (e.g., 'llama3.2:1b')."
    )
    args = parser.parse_args()

    pull_model(args.model)
