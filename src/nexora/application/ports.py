"""
Port definitions for the NEXORA AI platform.

Ports are interfaces that define contracts between the application core
and external adapters. They represent the boundaries of the hexagonal architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from nexora.domain.entities import (
    Dataset,
    Feature,
    Model,
    Explanation,
    Report,
    DataQuality,
)


class DataIngestionPort(ABC):
    """
    Port for data ingestion operations.

    Defines the interface for components that ingest data from various sources.
    """

    @abstractmethod
    def ingest(self, source_path: str, source_type: str) -> Dataset:
        """
        Ingest data from a source.

        Args:
            source_path: Path or connection string to the data source
            source_type: Type of data source (e.g., 'csv', 'json', 'parquet')

        Returns:
            Dataset object containing the ingested data

        Raises:
            IngestionException: If ingestion fails
        """
        pass

    @abstractmethod
    def validate_source(self, source_path: str, source_type: str) -> bool:
        """
        Validate that a data source is accessible and readable.

        Args:
            source_path: Path or connection string to the data source
            source_type: Type of data source

        Returns:
            True if source is valid, False otherwise
        """
        pass


class DataValidationPort(ABC):
    """
    Port for data validation operations.

    Defines the interface for components that validate data quality and integrity.
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass


class FeatureEngineeringPort(ABC):
    """
    Port for feature engineering operations.

    Defines the interface for components that engineer features from raw data.
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass


class ModelingPort(ABC):
    """
    Port for machine learning modeling operations.

    Defines the interface for components that train and use ML models.
    """

    @abstractmethod
    def train(
        self,
        dataset: Dataset,
        model_type: str,
        hyperparameters: Optional[dict[str, Any]] = None,
    ) -> Model:
        """
        Train a machine learning model.

        Args:
            dataset: Training dataset
            model_type: Type of model to train
            hyperparameters: Optional hyperparameters for the model

        Returns:
            Trained model

        Raises:
            ModelingException: If training fails
        """
        pass

    @abstractmethod
    def predict(self, model: Model, dataset: Dataset) -> Any:
        """
        Generate predictions using a trained model.

        Args:
            model: Trained model
            dataset: Dataset to predict on

        Returns:
            Predictions

        Raises:
            ModelingException: If prediction fails
        """
        pass

    @abstractmethod
    def evaluate(self, model: Model, dataset: Dataset) -> dict[str, float]:
        """
        Evaluate a model's performance.

        Args:
            model: Model to evaluate
            dataset: Evaluation dataset

        Returns:
            Dictionary of performance metrics

        Raises:
            ModelingException: If evaluation fails
        """
        pass


class ExplainabilityPort(ABC):
    """
    Port for model explainability operations.

    Defines the interface for components that explain model predictions.
    """

    @abstractmethod
    def explain_model(
        self, model: Model, dataset: Dataset, explanation_type: str
    ) -> Explanation:
        """
        Generate explanations for a model's behavior.

        Args:
            model: Model to explain
            dataset: Dataset used for explanation
            explanation_type: Type of explanation (e.g., 'shap', 'lime')

        Returns:
            Explanation object

        Raises:
            ExplainabilityException: If explanation generation fails
        """
        pass

    @abstractmethod
    def explain_prediction(
        self, model: Model, instance: dict[str, Any], explanation_type: str
    ) -> dict[str, Any]:
        """
        Explain a single prediction.

        Args:
            model: Model that made the prediction
            instance: Input instance to explain
            explanation_type: Type of explanation

        Returns:
            Explanation for the prediction

        Raises:
            ExplainabilityException: If explanation fails
        """
        pass


class GenAIPort(ABC):
    """
    Port for Generative AI operations.

    Defines the interface for components that interact with GenAI models.
    """

    @abstractmethod
    def generate_text(
        self, prompt: str, context: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Generate text using a GenAI model.

        Args:
            prompt: Input prompt
            context: Optional context for generation

        Returns:
            Generated text

        Raises:
            GenAIException: If generation fails
        """
        pass

    @abstractmethod
    def generate_insights(
        self, model: Model, explanation: Explanation
    ) -> dict[str, Any]:
        """
        Generate insights from model and explanations using GenAI.

        Args:
            model: Model to generate insights for
            explanation: Explanation data

        Returns:
            Generated insights

        Raises:
            GenAIException: If insight generation fails
        """
        pass


class ReportingPort(ABC):
    """
    Port for reporting operations.

    Defines the interface for components that generate reports.
    """

    @abstractmethod
    def generate_report(
        self,
        title: str,
        content: dict[str, Any],
        report_type: str,
        output_format: str = "markdown",
    ) -> Report:
        """
        Generate a report from provided content.

        Args:
            title: Report title
            content: Content to include in report
            report_type: Type of report
            output_format: Output format (e.g., 'markdown', 'html')

        Returns:
            Generated report

        Raises:
            ReportingException: If report generation fails
        """
        pass

    @abstractmethod
    def export_report(self, report: Report, output_path: str) -> str:
        """
        Export a report to a file.

        Args:
            report: Report to export
            output_path: Path to export to

        Returns:
            Path to exported report

        Raises:
            ReportingException: If export fails
        """
        pass
