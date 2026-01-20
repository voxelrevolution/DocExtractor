"""
tests/__init__.py
Test package initialization.
"""

import pytest
import os


@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables."""
    os.environ["APP_ENV"] = "testing"
    os.environ["PYTHONUNBUFFERED"] = "1"
