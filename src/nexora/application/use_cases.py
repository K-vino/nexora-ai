"""
Use cases for the NEXORA AI platform.

Use cases orchestrate business operations by coordinating between
different ports and domain entities.
"""

from typing import Any, Optional
from uuid import UUID

from nexora.core.exceptions import NexoraException
from nexora.core.logger import get_logger
from nexora.domain.entities import Dataset, Model, Report, WorkflowExecution
from nexora.application.ports import (
    DataIngestionPort,
    DataValidationPort,
    FeatureEngineeringPort,
    ModelingPort,
    ExplainabilityPort,
    GenAIPort,
    ReportingPort,
)

logger = get_logger(__name__)


class IngestDataUseCase:
    """
    Use case for ingesting data from external sources.
    """

    def __init__(
        self,
        ingestion_port: DataIngestionPort,
        validation_port: DataValidationPort,
    ) -> None:
        """
        Initialize the use case with required ports.

        Args:
            ingestion_port: Port for data ingestion
            validation_port: Port for data validation
        """
        self.ingestion_port = ingestion_port
        self.validation_port = validation_port

    def execute(self, source_path: str, source_type: str) -> Dataset:
        """
        Execute the data ingestion use case.

        Args:
            source_path: Path to the data source
            source_type: Type of data source

        Returns:
            Ingested and validated dataset

        Raises:
            NexoraException: If ingestion or validation fails
        """
        logger.info(f"Starting data ingestion from {source_path} ({source_type})")

        # Validate source
        if not self.ingestion_port.validate_source(source_path, source_type):
            raise NexoraException(f"Invalid data source: {source_path}")

        # Ingest data
        dataset = self.ingestion_port.ingest(source_path, source_type)
        logger.info(f"Ingested dataset: {dataset.name} with {dataset.row_count} rows")

        # Assess quality
        quality = self.validation_port.assess_quality(dataset)
        dataset.update_quality(quality)
        logger.info(f"Dataset quality assessed as: {quality.value}")

        return dataset


class TrainModelUseCase:
    """
    Use case for training machine learning models.
    """

    def __init__(
        self,
        feature_engineering_port: FeatureEngineeringPort,
        modeling_port: ModelingPort,
    ) -> None:
        """
        Initialize the use case with required ports.

        Args:
            feature_engineering_port: Port for feature engineering
            modeling_port: Port for modeling operations
        """
        self.feature_engineering_port = feature_engineering_port
        self.modeling_port = modeling_port

    def execute(
        self,
        dataset: Dataset,
        model_type: str,
        feature_specs: dict[str, Any],
        hyperparameters: Optional[dict[str, Any]] = None,
    ) -> Model:
        """
        Execute the model training use case.

        Args:
            dataset: Training dataset
            model_type: Type of model to train
            feature_specs: Specifications for feature engineering
            hyperparameters: Optional model hyperparameters

        Returns:
            Trained model

        Raises:
            NexoraException: If training fails
        """
        logger.info(f"Starting model training: {model_type}")

        # Engineer features
        features = self.feature_engineering_port.engineer_features(
            dataset, feature_specs
        )
        logger.info(f"Engineered {len(features)} features")

        # Transform dataset
        transformed_dataset = self.feature_engineering_port.transform(dataset, features)

        # Train model
        model = self.modeling_port.train(
            transformed_dataset, model_type, hyperparameters
        )
        logger.info(f"Model trained: {model.name} ({model.model_id})")

        return model


class ExplainModelUseCase:
    """
    Use case for explaining model predictions.
    """

    def __init__(
        self,
        explainability_port: ExplainabilityPort,
        genai_port: GenAIPort,
    ) -> None:
        """
        Initialize the use case with required ports.

        Args:
            explainability_port: Port for explainability operations
            genai_port: Port for GenAI operations
        """
        self.explainability_port = explainability_port
        self.genai_port = genai_port

    def execute(
        self,
        model: Model,
        dataset: Dataset,
        explanation_type: str = "shap",
    ) -> dict[str, Any]:
        """
        Execute the model explanation use case.

        Args:
            model: Model to explain
            dataset: Dataset for generating explanations
            explanation_type: Type of explanation to generate

        Returns:
            Dictionary containing explanation and insights

        Raises:
            NexoraException: If explanation generation fails
        """
        logger.info(f"Generating {explanation_type} explanations for model {model.name}")

        # Generate explanations
        explanation = self.explainability_port.explain_model(
            model, dataset, explanation_type
        )
        logger.info(f"Explanation generated: {explanation.explanation_id}")

        # Generate insights using GenAI
        insights = self.genai_port.generate_insights(model, explanation)
        logger.info("GenAI insights generated")

        return {
            "explanation": explanation,
            "insights": insights,
        }


class GenerateReportUseCase:
    """
    Use case for generating comprehensive reports.
    """

    def __init__(
        self,
        reporting_port: ReportingPort,
        genai_port: GenAIPort,
    ) -> None:
        """
        Initialize the use case with required ports.

        Args:
            reporting_port: Port for reporting operations
            genai_port: Port for GenAI operations
        """
        self.reporting_port = reporting_port
        self.genai_port = genai_port

    def execute(
        self,
        model: Model,
        explanation_data: dict[str, Any],
        output_format: str = "markdown",
    ) -> Report:
        """
        Execute the report generation use case.

        Args:
            model: Model to report on
            explanation_data: Explanation and insights data
            output_format: Desired output format

        Returns:
            Generated report

        Raises:
            NexoraException: If report generation fails
        """
        logger.info(f"Generating report for model {model.name}")

        # Prepare report content
        content = {
            "model": {
                "name": model.name,
                "type": model.model_type,
                "algorithm": model.algorithm,
                "metrics": model.performance_metrics,
            },
            "explanation": explanation_data.get("explanation"),
            "insights": explanation_data.get("insights"),
        }

        # Generate narrative using GenAI
        prompt = f"Generate a comprehensive report narrative for a {model.model_type} model"
        narrative = self.genai_port.generate_text(prompt, content)
        content["narrative"] = narrative

        # Generate report
        report = self.reporting_port.generate_report(
            title=f"Model Report: {model.name}",
            content=content,
            report_type="model_analysis",
            output_format=output_format,
        )
        logger.info(f"Report generated: {report.report_id}")

        return report
