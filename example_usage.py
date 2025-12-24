"""
Example usage demonstrating the NEXORA AI platform capabilities.

This script shows how to use the hexagonal architecture to build a complete
ML pipeline with data ingestion, feature engineering, modeling, explanation,
and reporting.
"""

from nexora.adapters.ingestion import FileIngestionAdapter
from nexora.adapters.validation import StandardValidationAdapter
from nexora.adapters.feature_engineering import StandardFeatureEngineeringAdapter
from nexora.adapters.modeling import SklearnModelingAdapter
from nexora.adapters.explainability import SHAPExplainabilityAdapter
from nexora.adapters.genai import PromptBasedGenAIAdapter
from nexora.adapters.reporting import MarkdownReportingAdapter
from nexora.application.use_cases import (
    IngestDataUseCase,
    TrainModelUseCase,
    ExplainModelUseCase,
    GenerateReportUseCase,
)
from nexora.core.logger import setup_logging, get_logger
from nexora.infrastructure.config import ConfigurationLoader
from nexora.orchestration import WorkflowBuilder, WorkflowOrchestrator

logger = get_logger(__name__)


def main() -> None:
    """Main execution function demonstrating the platform."""
    
    # Setup logging
    setup_logging()
    logger.info("Starting NEXORA AI example")

    # Load configuration
    config = ConfigurationLoader.get_default()
    logger.info(f"Configuration loaded: {config.app_name} ({config.environment})")

    # Initialize adapters
    ingestion_adapter = FileIngestionAdapter()
    validation_adapter = StandardValidationAdapter()
    feature_engineering_adapter = StandardFeatureEngineeringAdapter()
    modeling_adapter = SklearnModelingAdapter()
    explainability_adapter = SHAPExplainabilityAdapter()
    genai_adapter = PromptBasedGenAIAdapter()
    reporting_adapter = MarkdownReportingAdapter()

    # Initialize use cases
    ingest_use_case = IngestDataUseCase(ingestion_adapter, validation_adapter)
    train_use_case = TrainModelUseCase(feature_engineering_adapter, modeling_adapter)
    explain_use_case = ExplainModelUseCase(explainability_adapter, genai_adapter)
    report_use_case = GenerateReportUseCase(reporting_adapter, genai_adapter)

    logger.info("All adapters and use cases initialized")

    # Example workflow: Build and execute a complete ML pipeline
    logger.info("=" * 80)
    logger.info("Example 1: Simple workflow execution")
    logger.info("=" * 80)

    # Note: In a real scenario, you would provide actual data files
    # For this example, we demonstrate the structure and flow
    
    print("\n🚀 NEXORA AI - Enterprise Intelligence Platform")
    print("=" * 80)
    print("\n✅ System Architecture:")
    print("   - Core Layer: Base abstractions, exceptions, logging")
    print("   - Domain Layer: Business entities and value objects")
    print("   - Application Layer: Use cases and port definitions")
    print("   - Adapter Layer: Implementations for each concern")
    print("   - Infrastructure Layer: Configuration and utilities")
    print("   - Orchestration Layer: Workflow coordination")
    
    print("\n✅ Available Adapters:")
    print("   - Ingestion: File, Database")
    print("   - Validation: Standard, Schema-based")
    print("   - Feature Engineering: Standard, Time Series")
    print("   - Modeling: Scikit-learn, Deep Learning")
    print("   - Explainability: SHAP, LIME, Permutation Importance")
    print("   - GenAI: Local LLM, Prompt-based")
    print("   - Reporting: Markdown, HTML, JSON")

    print("\n✅ Use Cases:")
    print("   - IngestDataUseCase: Load and validate data")
    print("   - TrainModelUseCase: Feature engineering + model training")
    print("   - ExplainModelUseCase: Generate model explanations")
    print("   - GenerateReportUseCase: Create comprehensive reports")

    print("\n✅ Orchestration:")
    print("   - WorkflowOrchestrator: Coordinate multi-step workflows")
    print("   - WorkflowBuilder: Fluent API for workflow definition")
    
    print("\n" + "=" * 80)
    print("Example workflow orchestration:")
    print("=" * 80)

    # Build a workflow
    workflow = (
        WorkflowBuilder("ml_pipeline", "Complete ML pipeline workflow")
        .add_step("data_ingestion", lambda x: {"status": "ingested"})
        .add_step("data_validation", lambda x: {"status": "validated"}, dependencies=["data_ingestion"])
        .add_step("feature_engineering", lambda x: {"status": "features_created"}, dependencies=["data_validation"])
        .add_step("model_training", lambda x: {"status": "model_trained"}, dependencies=["feature_engineering"])
        .add_step("model_explanation", lambda x: {"status": "explained"}, dependencies=["model_training"])
        .add_step("report_generation", lambda x: {"status": "report_generated"}, dependencies=["model_explanation"])
        .build()
    )

    # Execute the workflow
    orchestrator = WorkflowOrchestrator()
    execution = orchestrator.execute_workflow(workflow)

    print(f"\n✅ Workflow Status: {execution.status.value}")
    print(f"   Steps Completed: {execution.steps_completed}/{execution.total_steps}")
    print(f"   Execution ID: {execution.execution_id}")
    
    print("\n" + "=" * 80)
    print("🎉 NEXORA AI platform is ready for development!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Implement actual adapter logic with real libraries")
    print("2. Add comprehensive tests for all components")
    print("3. Create domain-specific use cases")
    print("4. Build production workflows")
    print("5. Add monitoring and observability")
    print("\nFor more information, see the README.md file.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
