"""
Core module containing base abstractions, exceptions, and shared utilities.
"""

from .exceptions import (
    NexoraException,
    ValidationException,
    IngestionException,
    ModelingException,
    ExplainabilityException,
    ReportingException,
    ConfigurationException,
)
from .logger import get_logger, setup_logging

__all__ = [
    "NexoraException",
    "ValidationException",
    "IngestionException",
    "ModelingException",
    "ExplainabilityException",
    "ReportingException",
    "ConfigurationException",
    "get_logger",
    "setup_logging",
]
