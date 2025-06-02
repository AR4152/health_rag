# ------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2025 Arjun Raj
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

"""
MLHub Toolkit for health_rag - pull_model.

Author: Arjun Raj
Date: 2025-06-02
Version: 0.0.1

Command-line tool to pull LLM models via Ollama.

Usage:
    ml pull_nodel health_rag <model_name>
"""

import argparse
import subprocess


def pull_model(model: str):
    """
    Pulls a specified LLM model using the Ollama CLI.

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
