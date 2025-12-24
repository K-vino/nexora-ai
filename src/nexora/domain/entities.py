"""
Domain entities and value objects for the NEXORA AI platform.

This module contains the core business entities that represent
the domain model of the system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4


class DataQuality(Enum):
    """Enumeration of data quality levels."""

    UNKNOWN = "unknown"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class ProcessingStatus(Enum):
    """Enumeration of processing status states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class DataSource:
    """
    Value object representing a data source.

    Attributes:
        source_id: Unique identifier for the data source
        name: Human-readable name
        source_type: Type of data source (e.g., 'csv', 'json', 'database')
        location: Location or connection string
        metadata: Additional metadata about the source
    """

    source_id: UUID
    name: str
    source_type: str
    location: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Dataset:
    """
    Entity representing a dataset in the system.

    Attributes:
        dataset_id: Unique identifier
        name: Dataset name
        source: Origin of the data
        created_at: Creation timestamp
        updated_at: Last update timestamp
        quality: Data quality assessment
        row_count: Number of rows
        column_count: Number of columns
        schema: Schema definition
        metadata: Additional metadata
    """

    dataset_id: UUID = field(default_factory=uuid4)
    name: str = ""
    source: Optional[DataSource] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    quality: DataQuality = DataQuality.UNKNOWN
    row_count: int = 0
    column_count: int = 0
    schema: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def update_quality(self, quality: DataQuality) -> None:
        """Update the data quality assessment."""
        self.quality = quality
        self.updated_at = datetime.now()


@dataclass
class Feature:
    """
    Entity representing a feature engineered from data.

    Attributes:
        feature_id: Unique identifier
        name: Feature name
        feature_type: Data type of the feature
        description: Description of what the feature represents
        transformation: Description of the transformation applied
        importance: Feature importance score (if available)
        metadata: Additional metadata
    """

    feature_id: UUID = field(default_factory=uuid4)
    name: str = ""
    feature_type: str = "numeric"
    description: str = ""
    transformation: str = ""
    importance: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Model:
    """
    Entity representing a machine learning model.

    Attributes:
        model_id: Unique identifier
        name: Model name
        model_type: Type of model (e.g., 'classification', 'regression')
        algorithm: Algorithm used
        version: Model version
        created_at: Creation timestamp
        trained_at: Training completion timestamp
        performance_metrics: Model performance metrics
        hyperparameters: Model hyperparameters
        metadata: Additional metadata
    """

    model_id: UUID = field(default_factory=uuid4)
    name: str = ""
    model_type: str = ""
    algorithm: str = ""
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    trained_at: Optional[datetime] = None
    performance_metrics: dict[str, float] = field(default_factory=dict)
    hyperparameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def update_metrics(self, metrics: dict[str, float]) -> None:
        """Update model performance metrics."""
        self.performance_metrics.update(metrics)


@dataclass
class Explanation:
    """
    Entity representing a model explanation.

    Attributes:
        explanation_id: Unique identifier
        model_id: Associated model identifier
        explanation_type: Type of explanation (e.g., 'shap', 'lime')
        feature_importance: Feature importance scores
        created_at: Creation timestamp
        content: Explanation content
        metadata: Additional metadata
    """

    explanation_id: UUID = field(default_factory=uuid4)
    model_id: UUID = field(default_factory=uuid4)
    explanation_type: str = ""
    feature_importance: dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    content: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    """
    Entity representing a generated report.

    Attributes:
        report_id: Unique identifier
        title: Report title
        report_type: Type of report
        created_at: Creation timestamp
        content: Report content
        format: Output format (e.g., 'markdown', 'html', 'pdf')
        metadata: Additional metadata
    """

    report_id: UUID = field(default_factory=uuid4)
    title: str = ""
    report_type: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    content: str = ""
    format: str = "markdown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """
    Entity representing a workflow execution.

    Attributes:
        execution_id: Unique identifier
        workflow_name: Name of the workflow
        status: Current execution status
        started_at: Start timestamp
        completed_at: Completion timestamp
        steps_completed: Number of steps completed
        total_steps: Total number of steps
        result: Execution result
        error: Error information if failed
        metadata: Additional metadata
    """

    execution_id: UUID = field(default_factory=uuid4)
    workflow_name: str = ""
    status: ProcessingStatus = ProcessingStatus.PENDING
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    steps_completed: int = 0
    total_steps: int = 0
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def mark_completed(self, result: dict[str, Any]) -> None:
        """Mark execution as completed with result."""
        self.status = ProcessingStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def mark_failed(self, error: str) -> None:
        """Mark execution as failed with error message."""
        self.status = ProcessingStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
