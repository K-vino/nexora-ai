"""
Base abstractions for the NEXORA AI platform.

This module contains abstract base classes that define interfaces for all major
components following the hexagonal architecture pattern.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

# Type variables for generic abstractions
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")
TConfig = TypeVar("TConfig")


class BaseProcessor(ABC, Generic[TInput, TOutput]):
    """
    Abstract base class for all data processors.

    This class defines the interface for components that transform data
    from one form to another.
    """

    @abstractmethod
    def process(self, data: TInput) -> TOutput:
        """
        Process input data and return transformed output.

        Args:
            data: Input data to process

        Returns:
            Processed output data

        Raises:
            NexoraException: If processing fails
        """
        pass

    @abstractmethod
    def validate_input(self, data: TInput) -> bool:
        """
        Validate that input data meets requirements.

        Args:
            data: Input data to validate

        Returns:
            True if valid, False otherwise
        """
        pass


class BaseRepository(ABC, Generic[TInput]):
    """
    Abstract base class for data repositories.

    This class defines the interface for components that handle data persistence
    and retrieval operations.
    """

    @abstractmethod
    def save(self, data: TInput) -> str:
        """
        Persist data to the repository.

        Args:
            data: Data to save

        Returns:
            Unique identifier for the saved data

        Raises:
            NexoraException: If save operation fails
        """
        pass

    @abstractmethod
    def load(self, identifier: str) -> TInput:
        """
        Load data from the repository.

        Args:
            identifier: Unique identifier of the data to load

        Returns:
            Retrieved data

        Raises:
            NexoraException: If load operation fails
        """
        pass

    @abstractmethod
    def exists(self, identifier: str) -> bool:
        """
        Check if data exists in the repository.

        Args:
            identifier: Unique identifier to check

        Returns:
            True if exists, False otherwise
        """
        pass


class BaseService(ABC):
    """
    Abstract base class for application services.

    Services orchestrate business logic and coordinate between
    different components of the system.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service and its dependencies.

        Raises:
            NexoraException: If initialization fails
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        Gracefully shutdown the service and clean up resources.

        Raises:
            NexoraException: If shutdown fails
        """
        pass


class Configurable(ABC, Generic[TConfig]):
    """
    Abstract base class for configurable components.

    Components implementing this interface can be configured
    with specific settings.
    """

    @abstractmethod
    def configure(self, config: TConfig) -> None:
        """
        Configure the component with given settings.

        Args:
            config: Configuration object

        Raises:
            ConfigurationException: If configuration is invalid
        """
        pass

    @abstractmethod
    def get_config(self) -> TConfig:
        """
        Get the current configuration.

        Returns:
            Current configuration object
        """
        pass


class BaseAdapter(ABC, Generic[TInput, TOutput]):
    """
    Abstract base class for adapters.

    Adapters translate between the application's internal model
    and external systems or formats.
    """

    @abstractmethod
    def adapt(self, data: TInput) -> TOutput:
        """
        Adapt data from one format to another.

        Args:
            data: Input data in source format

        Returns:
            Data in target format

        Raises:
            NexoraException: If adaptation fails
        """
        pass
