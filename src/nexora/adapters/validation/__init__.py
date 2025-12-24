"""
Data validation adapters for quality assessment and validation rules.
"""

from typing import Any

from nexora.application.ports import DataValidationPort
from nexora.core.exceptions import ValidationException
from nexora.core.logger import get_logger
from nexora.domain.entities import Dataset, DataQuality

logger = get_logger(__name__)


class StandardValidationAdapter(DataValidationPort):
    """
    Standard validation adapter implementing common validation rules.

    Validates data completeness, consistency, and basic quality checks.
    """

    def __init__(self, validation_rules: dict[str, Any] | None = None) -> None:
        """
        Initialize the validation adapter.

        Args:
            validation_rules: Optional custom validation rules
        """
        self.validation_rules = validation_rules or {}
        logger.info("StandardValidationAdapter initialized")

    def validate(self, dataset: Dataset) -> tuple[bool, dict[str, Any]]:
        """
        Validate a dataset for quality and integrity.

        Args:
            dataset: Dataset to validate

        Returns:
            Tuple of (is_valid, validation_report)

        Raises:
            ValidationException: If validation process fails
        """
        try:
            validation_report: dict[str, Any] = {
                "dataset_id": str(dataset.dataset_id),
                "dataset_name": dataset.name,
                "checks": {},
                "issues": [],
            }

            # Check 1: Dataset has rows
            has_rows = dataset.row_count > 0
            validation_report["checks"]["has_rows"] = has_rows
            if not has_rows:
                validation_report["issues"].append("Dataset has no rows")

            # Check 2: Dataset has columns
            has_columns = dataset.column_count > 0
            validation_report["checks"]["has_columns"] = has_columns
            if not has_columns:
                validation_report["issues"].append("Dataset has no columns")

            # Check 3: Schema is defined
            has_schema = len(dataset.schema) > 0
            validation_report["checks"]["has_schema"] = has_schema
            if not has_schema:
                validation_report["issues"].append("Dataset schema is not defined")

            # Overall validation
            is_valid = has_rows and has_columns and has_schema

            validation_report["is_valid"] = is_valid
            validation_report["issues_count"] = len(validation_report["issues"])

            logger.info(
                f"Validation completed for dataset {dataset.name}: "
                f"{'valid' if is_valid else 'invalid'}"
            )

            return is_valid, validation_report

        except Exception as e:
            raise ValidationException(
                f"Failed to validate dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )

    def assess_quality(self, dataset: Dataset) -> DataQuality:
        """
        Assess the quality level of a dataset.

        Args:
            dataset: Dataset to assess

        Returns:
            DataQuality level

        Raises:
            ValidationException: If assessment fails
        """
        try:
            # Simple quality assessment based on completeness
            if dataset.row_count == 0 or dataset.column_count == 0:
                return DataQuality.POOR

            if len(dataset.schema) == 0:
                return DataQuality.FAIR

            # Check data completeness (in production, would check actual data)
            if dataset.row_count < 100:
                return DataQuality.FAIR
            elif dataset.row_count < 1000:
                return DataQuality.GOOD
            else:
                return DataQuality.EXCELLENT

        except Exception as e:
            raise ValidationException(
                f"Failed to assess quality for dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )


class SchemaValidationAdapter(DataValidationPort):
    """
    Schema-based validation adapter for enforcing data schemas.

    Validates that data conforms to expected schemas and types.
    """

    def __init__(self, expected_schema: dict[str, str]) -> None:
        """
        Initialize the schema validation adapter.

        Args:
            expected_schema: Expected schema definition
        """
        self.expected_schema = expected_schema
        logger.info("SchemaValidationAdapter initialized")

    def validate(self, dataset: Dataset) -> tuple[bool, dict[str, Any]]:
        """
        Validate dataset against expected schema.

        Args:
            dataset: Dataset to validate

        Returns:
            Tuple of (is_valid, validation_report)

        Raises:
            ValidationException: If validation process fails
        """
        try:
            validation_report: dict[str, Any] = {
                "dataset_id": str(dataset.dataset_id),
                "dataset_name": dataset.name,
                "schema_validation": {},
                "issues": [],
            }

            # Check if all expected columns are present
            missing_columns = set(self.expected_schema.keys()) - set(
                dataset.schema.keys()
            )
            extra_columns = set(dataset.schema.keys()) - set(
                self.expected_schema.keys()
            )

            if missing_columns:
                validation_report["issues"].append(
                    f"Missing columns: {missing_columns}"
                )

            if extra_columns:
                validation_report["issues"].append(f"Extra columns: {extra_columns}")

            # Check column types
            type_mismatches = []
            for col, expected_type in self.expected_schema.items():
                if col in dataset.schema:
                    actual_type = dataset.schema[col]
                    if actual_type != expected_type:
                        type_mismatches.append(
                            f"{col}: expected {expected_type}, got {actual_type}"
                        )

            if type_mismatches:
                validation_report["issues"].append(f"Type mismatches: {type_mismatches}")

            is_valid = len(validation_report["issues"]) == 0
            validation_report["is_valid"] = is_valid

            return is_valid, validation_report

        except Exception as e:
            raise ValidationException(
                f"Failed schema validation for dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )

    def assess_quality(self, dataset: Dataset) -> DataQuality:
        """
        Assess quality based on schema conformance.

        Args:
            dataset: Dataset to assess

        Returns:
            DataQuality level
        """
        is_valid, report = self.validate(dataset)

        if is_valid:
            return DataQuality.EXCELLENT
        elif len(report["issues"]) <= 2:
            return DataQuality.GOOD
        elif len(report["issues"]) <= 5:
            return DataQuality.FAIR
        else:
            return DataQuality.POOR
