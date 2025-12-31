class NexoraError(Exception):
    """Base exception for all Nexora AI errors."""
    pass

class DataIngestionError(NexoraError):
    """Raised when data loading fails."""
    pass

class ValidationError(NexoraError):
    """Raised when data validation fails."""
    pass

class FeatureEngineeringError(NexoraError):
    """Raised when feature engineering fails."""
    pass

class ModelingError(NexoraError):
    """Raised when model training or prediction fails."""
    pass

class ConfigurationError(NexoraError):
    """Raised when configuration is invalid."""
    pass
