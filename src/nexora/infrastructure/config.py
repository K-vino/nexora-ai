"""
Configuration management for the NEXORA AI platform.

Provides centralized configuration loading and management.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import json

from nexora.core.exceptions import ConfigurationException
from nexora.core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Configuration:
    """
    Main configuration object for the NEXORA AI platform.

    Attributes:
        app_name: Application name
        environment: Environment (e.g., 'development', 'production')
        log_level: Logging level
        data_directory: Directory for data storage
        model_directory: Directory for model storage
        report_directory: Directory for report output
        custom_settings: Additional custom settings
    """

    app_name: str = "NEXORA AI"
    environment: str = "development"
    log_level: str = "INFO"
    data_directory: str = "./data"
    model_directory: str = "./models"
    report_directory: str = "./reports"
    custom_settings: dict[str, Any] = field(default_factory=dict)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a custom setting by key.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        return self.custom_settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """
        Set a custom setting.

        Args:
            key: Setting key
            value: Setting value
        """
        self.custom_settings[key] = value

    def validate(self) -> bool:
        """
        Validate the configuration.

        Returns:
            True if valid, False otherwise
        """
        if not self.app_name:
            logger.error("Configuration validation failed: app_name is required")
            return False

        if self.environment not in ["development", "staging", "production"]:
            logger.warning(f"Unusual environment: {self.environment}")

        return True


class ConfigurationLoader:
    """
    Utility class for loading configuration from various sources.

    Supports loading from JSON files, environment variables, and dictionaries.
    """

    @staticmethod
    def from_file(file_path: str) -> Configuration:
        """
        Load configuration from a JSON file.

        Args:
            file_path: Path to the configuration file

        Returns:
            Configuration object

        Raises:
            ConfigurationException: If loading fails
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise ConfigurationException(
                    f"Configuration file not found: {file_path}",
                    details={"file_path": file_path},
                )

            with open(path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            config = Configuration(**config_data)

            if not config.validate():
                raise ConfigurationException(
                    "Configuration validation failed",
                    details={"file_path": file_path},
                )

            logger.info(f"Configuration loaded from {file_path}")
            return config

        except json.JSONDecodeError as e:
            raise ConfigurationException(
                f"Invalid JSON in configuration file: {file_path}",
                details={"file_path": file_path},
                original_exception=e,
            )
        except Exception as e:
            raise ConfigurationException(
                f"Failed to load configuration from {file_path}",
                details={"file_path": file_path},
                original_exception=e,
            )

    @staticmethod
    def from_dict(config_dict: dict[str, Any]) -> Configuration:
        """
        Create configuration from a dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Configuration object

        Raises:
            ConfigurationException: If creation fails
        """
        try:
            config = Configuration(**config_dict)

            if not config.validate():
                raise ConfigurationException(
                    "Configuration validation failed",
                    details={"source": "dictionary"},
                )

            logger.info("Configuration created from dictionary")
            return config

        except Exception as e:
            raise ConfigurationException(
                "Failed to create configuration from dictionary",
                details={"source": "dictionary"},
                original_exception=e,
            )

    @staticmethod
    def from_env() -> Configuration:
        """
        Load configuration from environment variables.

        Returns:
            Configuration object

        Raises:
            ConfigurationException: If loading fails
        """
        import os

        try:
            config = Configuration(
                app_name=os.getenv("NEXORA_APP_NAME", "NEXORA AI"),
                environment=os.getenv("NEXORA_ENVIRONMENT", "development"),
                log_level=os.getenv("NEXORA_LOG_LEVEL", "INFO"),
                data_directory=os.getenv("NEXORA_DATA_DIR", "./data"),
                model_directory=os.getenv("NEXORA_MODEL_DIR", "./models"),
                report_directory=os.getenv("NEXORA_REPORT_DIR", "./reports"),
            )

            if not config.validate():
                raise ConfigurationException(
                    "Configuration validation failed",
                    details={"source": "environment"},
                )

            logger.info("Configuration loaded from environment variables")
            return config

        except Exception as e:
            raise ConfigurationException(
                "Failed to load configuration from environment",
                details={"source": "environment"},
                original_exception=e,
            )

    @staticmethod
    def get_default() -> Configuration:
        """
        Get default configuration.

        Returns:
            Default configuration object
        """
        config = Configuration()
        logger.info("Using default configuration")
        return config
