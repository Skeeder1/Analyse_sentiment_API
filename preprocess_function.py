"""Compatibility wrapper for preprocessing.

Imports the implementation from the `src.api_analyse` package so existing tests
or imports that reference `preprocess_function.preprocess_text` keep working.
"""

from src.api_analyse.preprocess import preprocess_text

__all__ = ["preprocess_text"]

