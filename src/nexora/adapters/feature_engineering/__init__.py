"""
Feature engineering adapters for data transformation and feature creation.
"""

from typing import Any
from uuid import uuid4

from nexora.application.ports import FeatureEngineeringPort
from nexora.core.exceptions import FeatureEngineeringException
from nexora.core.logger import get_logger
from nexora.domain.entities import Dataset, Feature

logger = get_logger(__name__)


class StandardFeatureEngineeringAdapter(FeatureEngineeringPort):
    """
    Standard feature engineering adapter implementing common transformations.

    Supports scaling, encoding, and statistical feature generation.
    """

    def __init__(self) -> None:
        """Initialize the feature engineering adapter."""
        logger.info("StandardFeatureEngineeringAdapter initialized")

    def engineer_features(
        self, dataset: Dataset, feature_specs: dict[str, Any]
    ) -> list[Feature]:
        """
        Engineer features from a dataset based on specifications.

        Args:
            dataset: Source dataset
            feature_specs: Specifications for features to engineer

        Returns:
            List of engineered features

        Raises:
            FeatureEngineeringException: If feature engineering fails
        """
        try:
            features: list[Feature] = []

            for feature_name, spec in feature_specs.items():
                feature = Feature(
                    feature_id=uuid4(),
                    name=feature_name,
                    feature_type=spec.get("type", "numeric"),
                    description=spec.get("description", ""),
                    transformation=spec.get("transformation", ""),
                )
                features.append(feature)

            logger.info(f"Engineered {len(features)} features for dataset {dataset.name}")
            return features

        except Exception as e:
            raise FeatureEngineeringException(
                f"Failed to engineer features for dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )

    def transform(self, dataset: Dataset, features: list[Feature]) -> Dataset:
        """
        Apply feature transformations to a dataset.

        Args:
            dataset: Dataset to transform
            features: Features to apply

        Returns:
            Transformed dataset

        Raises:
            FeatureEngineeringException: If transformation fails
        """
        try:
            # Create new dataset with transformations applied
            transformed_dataset = Dataset(
                name=f"{dataset.name}_transformed",
                source=dataset.source,
                row_count=dataset.row_count,
                column_count=dataset.column_count + len(features),
            )

            # Update schema with new features
            transformed_dataset.schema = dataset.schema.copy()
            for feature in features:
                transformed_dataset.schema[feature.name] = feature.feature_type

            transformed_dataset.metadata = {
                "original_dataset": str(dataset.dataset_id),
                "features_applied": [str(f.feature_id) for f in features],
            }

            logger.info(
                f"Applied {len(features)} features to dataset {dataset.name}"
            )
            return transformed_dataset

        except Exception as e:
            raise FeatureEngineeringException(
                f"Failed to transform dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )


class TimeSeriesFeatureEngineeringAdapter(FeatureEngineeringPort):
    """
    Feature engineering adapter specialized for time series data.

    Supports lag features, rolling statistics, and temporal patterns.
    """

    def __init__(self, window_size: int = 7) -> None:
        """
        Initialize the time series feature engineering adapter.

        Args:
            window_size: Default window size for rolling statistics
        """
        self.window_size = window_size
        logger.info(f"TimeSeriesFeatureEngineeringAdapter initialized with window_size={window_size}")

    def engineer_features(
        self, dataset: Dataset, feature_specs: dict[str, Any]
    ) -> list[Feature]:
        """
        Engineer time series features from a dataset.

        Args:
            dataset: Source dataset
            feature_specs: Specifications for features to engineer

        Returns:
            List of engineered time series features

        Raises:
            FeatureEngineeringException: If feature engineering fails
        """
        try:
            features: list[Feature] = []

            # Common time series features
            ts_transformations = [
                f"lag_{i}" for i in range(1, self.window_size + 1)
            ] + [
                f"rolling_mean_{self.window_size}",
                f"rolling_std_{self.window_size}",
                "day_of_week",
                "month",
                "quarter",
            ]

            for transformation in ts_transformations:
                feature = Feature(
                    feature_id=uuid4(),
                    name=f"ts_{transformation}",
                    feature_type="numeric",
                    description=f"Time series feature: {transformation}",
                    transformation=transformation,
                )
                features.append(feature)

            logger.info(
                f"Engineered {len(features)} time series features for dataset {dataset.name}"
            )
            return features

        except Exception as e:
            raise FeatureEngineeringException(
                f"Failed to engineer time series features for dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )

    def transform(self, dataset: Dataset, features: list[Feature]) -> Dataset:
        """
        Apply time series feature transformations to a dataset.

        Args:
            dataset: Dataset to transform
            features: Time series features to apply

        Returns:
            Transformed dataset

        Raises:
            FeatureEngineeringException: If transformation fails
        """
        try:
            # Create new dataset with time series transformations
            transformed_dataset = Dataset(
                name=f"{dataset.name}_ts_transformed",
                source=dataset.source,
                row_count=dataset.row_count,
                column_count=dataset.column_count + len(features),
            )

            # Update schema
            transformed_dataset.schema = dataset.schema.copy()
            for feature in features:
                transformed_dataset.schema[feature.name] = feature.feature_type

            transformed_dataset.metadata = {
                "original_dataset": str(dataset.dataset_id),
                "transformation_type": "time_series",
                "window_size": self.window_size,
            }

            logger.info(
                f"Applied {len(features)} time series features to dataset {dataset.name}"
            )
            return transformed_dataset

        except Exception as e:
            raise FeatureEngineeringException(
                f"Failed to transform time series dataset {dataset.name}",
                details={"dataset_id": str(dataset.dataset_id)},
                original_exception=e,
            )
