"""
Custom exceptions for the NEXORA AI platform.

This module defines a hierarchy of exceptions that provide clear error handling
across all layers of the application.
"""

from typing import Optional, Any


class NexoraException(Exception):
    """Base exception for all NEXORA AI errors."""

    def __init__(
        self,
        message: str,
        details: Optional[dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize NexoraException.

        Args:
            message: Human-readable error message
            details: Additional context about the error
            original_exception: The original exception if this wraps another error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_exception = original_exception

    def __str__(self) -> str:
        """Return string representation of the exception."""
        base = self.message
        if self.details:
            base += f" | Details: {self.details}"
        if self.original_exception:
            base += f" | Caused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return base


class ValidationException(NexoraException):
    """Exception raised during data validation operations."""

    pass


class IngestionException(NexoraException):
    """Exception raised during data ingestion operations."""

    pass


class ModelingException(NexoraException):
    """Exception raised during machine learning modeling operations."""

    pass


class ExplainabilityException(NexoraException):
    """Exception raised during model explainability operations."""

    pass


class ReportingException(NexoraException):
    """Exception raised during report generation operations."""

    pass


class ConfigurationException(NexoraException):
    """Exception raised for configuration-related errors."""

    pass


class FeatureEngineeringException(NexoraException):
    """Exception raised during feature engineering operations."""

    pass


class GenAIException(NexoraException):
    """Exception raised during GenAI operations."""

    pass


class OrchestrationException(NexoraException):
    """Exception raised during workflow orchestration operations."""

    pass
