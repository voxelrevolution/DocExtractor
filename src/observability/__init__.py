"""
src/observability/__init__.py
OpenTelemetry initialization and instrumentation.
"""

import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

logger = logging.getLogger(__name__)


def init_telemetry(otlp_endpoint: str = "http://localhost:4317") -> TracerProvider:
    """
    Initialize OpenTelemetry tracing and metrics.

    Args:
        otlp_endpoint: OTLP collector endpoint

    Returns:
        Configured TracerProvider
    """
    try:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        trace_provider = TracerProvider()
        trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(trace_provider)
        logger.info(f"Telemetry initialized with endpoint: {otlp_endpoint}")
        return trace_provider
    except Exception as e:
        logger.warning(f"Telemetry initialization failed: {e}. Continuing with defaults.")
        return TracerProvider()


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer instance."""
    return trace.get_tracer(name)
