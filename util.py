"""Utility functions for path normalization and related helpers."""

import os

from mlhub import get_cmd_cwd


def normalize_path(input_path: str) -> str:
    """Return an absolute path by ensuring the input path is fully qualified.

    If the input path is already absolute, it is returned unchanged.
    If it is a relative path, it is prepended with the current working directory
    obtained from get_cmd_cwd().

    Args:
        input_path (str): The file or directory path to normalize.

    Returns:
        str: An absolute path.

    """
    if os.path.isabs(input_path):
        return input_path
    else:
        return os.path.join(get_cmd_cwd(), input_path)
