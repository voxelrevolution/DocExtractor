"""
src/__init__.py
Initialize the DocExtractor package.
"""

__version__ = "0.1.0"
__author__ = "DocExtractor Team"

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
