"""
Unit tests for core exceptions module.
"""

import pytest

from nexora.core.exceptions import (
    NexoraException,
    ValidationException,
    IngestionException,
    ModelingException,
    ExplainabilityException,
    ReportingException,
    ConfigurationException,
)


class TestNexoraException:
    """Tests for the base NexoraException class."""

    def test_basic_exception(self):
        """Test creating a basic exception."""
        exc = NexoraException("Test error")
        assert exc.message == "Test error"
        assert exc.details == {}
        assert exc.original_exception is None

    def test_exception_with_details(self):
        """Test exception with details."""
        details = {"key": "value", "number": 42}
        exc = NexoraException("Test error", details=details)
        assert exc.details == details

    def test_exception_with_original(self):
        """Test exception wrapping another exception."""
        original = ValueError("Original error")
        exc = NexoraException("Test error", original_exception=original)
        assert exc.original_exception is original

    def test_exception_string_representation(self):
        """Test string representation of exception."""
        exc = NexoraException("Test error")
        assert "Test error" in str(exc)

        exc_with_details = NexoraException("Test error", details={"key": "value"})
        exc_str = str(exc_with_details)
        assert "Test error" in exc_str
        assert "Details:" in exc_str


class TestSpecificExceptions:
    """Tests for specific exception types."""

    def test_validation_exception(self):
        """Test ValidationException."""
        exc = ValidationException("Validation failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Validation failed"

    def test_ingestion_exception(self):
        """Test IngestionException."""
        exc = IngestionException("Ingestion failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Ingestion failed"

    def test_modeling_exception(self):
        """Test ModelingException."""
        exc = ModelingException("Modeling failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Modeling failed"

    def test_explainability_exception(self):
        """Test ExplainabilityException."""
        exc = ExplainabilityException("Explainability failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Explainability failed"

    def test_reporting_exception(self):
        """Test ReportingException."""
        exc = ReportingException("Reporting failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Reporting failed"

    def test_configuration_exception(self):
        """Test ConfigurationException."""
        exc = ConfigurationException("Configuration failed")
        assert isinstance(exc, NexoraException)
        assert exc.message == "Configuration failed"
