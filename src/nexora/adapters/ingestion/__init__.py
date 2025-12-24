"""
Data ingestion adapters for various data sources.
"""

from pathlib import Path
from typing import Any
from uuid import uuid4

from nexora.application.ports import DataIngestionPort
from nexora.core.exceptions import IngestionException
from nexora.core.logger import get_logger
from nexora.domain.entities import Dataset, DataSource

logger = get_logger(__name__)


class FileIngestionAdapter(DataIngestionPort):
    """
    Adapter for ingesting data from local files.

    Supports various file formats like CSV, JSON, and Parquet.
    """

    SUPPORTED_TYPES = {"csv", "json", "parquet", "txt"}

    def __init__(self) -> None:
        """Initialize the file ingestion adapter."""
        logger.info("FileIngestionAdapter initialized")

    def validate_source(self, source_path: str, source_type: str) -> bool:
        """
        Validate that a file source is accessible and of supported type.

        Args:
            source_path: Path to the file
            source_type: Type of file

        Returns:
            True if source is valid, False otherwise
        """
        if source_type not in self.SUPPORTED_TYPES:
            logger.warning(f"Unsupported source type: {source_type}")
            return False

        path = Path(source_path)
        if not path.exists():
            logger.warning(f"Source file does not exist: {source_path}")
            return False

        if not path.is_file():
            logger.warning(f"Source path is not a file: {source_path}")
            return False

        return True

    def ingest(self, source_path: str, source_type: str) -> Dataset:
        """
        Ingest data from a file source.

        Args:
            source_path: Path to the file
            source_type: Type of file

        Returns:
            Dataset object containing the ingested data

        Raises:
            IngestionException: If ingestion fails
        """
        if not self.validate_source(source_path, source_type):
            raise IngestionException(
                f"Invalid source: {source_path}",
                details={"source_path": source_path, "source_type": source_type},
            )

        try:
            path = Path(source_path)
            
            # Create data source
            data_source = DataSource(
                source_id=uuid4(),
                name=path.name,
                source_type=source_type,
                location=source_path,
            )

            # Create dataset (in production, would actually read the file)
            dataset = Dataset(
                name=path.stem,
                source=data_source,
            )

            # Simulate reading file metadata
            dataset.metadata = {
                "file_size": path.stat().st_size,
                "file_path": str(path.absolute()),
            }

            logger.info(f"Successfully ingested data from {source_path}")
            return dataset

        except Exception as e:
            raise IngestionException(
                f"Failed to ingest data from {source_path}",
                details={"source_path": source_path, "source_type": source_type},
                original_exception=e,
            )


class DatabaseIngestionAdapter(DataIngestionPort):
    """
    Adapter for ingesting data from databases.

    Supports various database connections through connection strings.
    """

    SUPPORTED_TYPES = {"postgresql", "mysql", "sqlite", "mongodb"}

    def __init__(self) -> None:
        """Initialize the database ingestion adapter."""
        logger.info("DatabaseIngestionAdapter initialized")

    def validate_source(self, source_path: str, source_type: str) -> bool:
        """
        Validate database connection string and type.

        Args:
            source_path: Database connection string
            source_type: Type of database

        Returns:
            True if source is valid, False otherwise
        """
        if source_type not in self.SUPPORTED_TYPES:
            logger.warning(f"Unsupported database type: {source_type}")
            return False

        # In production, would test actual connection
        if not source_path:
            logger.warning("Empty connection string provided")
            return False

        return True

    def ingest(self, source_path: str, source_type: str) -> Dataset:
        """
        Ingest data from a database.

        Args:
            source_path: Database connection string
            source_type: Type of database

        Returns:
            Dataset object containing the ingested data

        Raises:
            IngestionException: If ingestion fails
        """
        if not self.validate_source(source_path, source_type):
            raise IngestionException(
                f"Invalid database source: {source_type}",
                details={"source_path": source_path, "source_type": source_type},
            )

        try:
            # Create data source
            data_source = DataSource(
                source_id=uuid4(),
                name=f"{source_type}_database",
                source_type=source_type,
                location=source_path,
            )

            # Create dataset (in production, would execute query)
            dataset = Dataset(
                name=f"{source_type}_data",
                source=data_source,
            )

            logger.info(f"Successfully ingested data from {source_type} database")
            return dataset

        except Exception as e:
            raise IngestionException(
                f"Failed to ingest data from database",
                details={"source_path": source_path, "source_type": source_type},
                original_exception=e,
            )
