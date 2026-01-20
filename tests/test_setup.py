"""
tests/test_setup.py
Smoke tests to verify environment setup.
"""

import pytest
import sys
import subprocess


def test_python_version():
    """Verify Python 3.11+"""
    assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"


def test_fastapi_import():
    """Verify FastAPI is installed."""
    try:
        import fastapi

        assert hasattr(fastapi, "FastAPI")
    except ImportError:
        pytest.fail("FastAPI not installed")


def test_pydantic_import():
    """Verify Pydantic is installed."""
    try:
        import pydantic

        assert hasattr(pydantic, "BaseModel")
    except ImportError:
        pytest.fail("Pydantic not installed")


def test_sqlalchemy_import():
    """Verify SQLAlchemy is installed."""
    try:
        import sqlalchemy

        assert hasattr(sqlalchemy, "create_engine")
    except ImportError:
        pytest.fail("SQLAlchemy not installed")


def test_opentelemetry_import():
    """Verify OpenTelemetry is installed."""
    try:
        from opentelemetry import trace

        assert trace.get_tracer is not None
    except ImportError:
        pytest.fail("OpenTelemetry not installed")


def test_pytest_asyncio():
    """Verify pytest-asyncio is available."""
    try:
        import pytest_asyncio

        assert pytest_asyncio is not None
    except ImportError:
        pytest.fail("pytest-asyncio not installed")


@pytest.mark.asyncio
async def test_async_support():
    """Verify async/await works."""
    async def dummy_async():
        return True

    result = await dummy_async()
    assert result is True


def test_venv_active():
    """Verify we're running in a virtual environment."""
    # Check if sys.prefix != sys.base_prefix (indicating venv)
    in_venv = sys.prefix != sys.base_prefix
    # Or check for VIRTUAL_ENV env var
    import os

    has_venv_env = "VIRTUAL_ENV" in os.environ
    assert in_venv or has_venv_env, "Not running in a virtual environment"


def test_docker_available():
    """Check if Docker is available (not required, but recommended)."""
    try:
        result = subprocess.run(
            ["docker", "--version"], capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0, "Docker not available"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("Docker not available (optional)")


def test_ollama_available():
    """Check if Ollama is available (not required, but recommended)."""
    try:
        result = subprocess.run(
            ["ollama", "--version"], capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0, "Ollama not available"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("Ollama not available (optional)")
