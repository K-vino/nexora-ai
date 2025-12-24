"""
Unit tests for domain entities.
"""

import pytest
from datetime import datetime
from uuid import UUID

from nexora.domain.entities import (
    DataQuality,
    ProcessingStatus,
    DataSource,
    Dataset,
    Feature,
    Model,
    Explanation,
    Report,
    WorkflowExecution,
)


class TestDataQuality:
    """Tests for DataQuality enum."""

    def test_data_quality_values(self):
        """Test DataQuality enum values."""
        assert DataQuality.UNKNOWN.value == "unknown"
        assert DataQuality.POOR.value == "poor"
        assert DataQuality.FAIR.value == "fair"
        assert DataQuality.GOOD.value == "good"
        assert DataQuality.EXCELLENT.value == "excellent"


class TestProcessingStatus:
    """Tests for ProcessingStatus enum."""

    def test_processing_status_values(self):
        """Test ProcessingStatus enum values."""
        assert ProcessingStatus.PENDING.value == "pending"
        assert ProcessingStatus.IN_PROGRESS.value == "in_progress"
        assert ProcessingStatus.COMPLETED.value == "completed"
        assert ProcessingStatus.FAILED.value == "failed"
        assert ProcessingStatus.CANCELLED.value == "cancelled"


class TestDataSource:
    """Tests for DataSource value object."""

    def test_data_source_creation(self):
        """Test creating a DataSource."""
        from uuid import uuid4

        source_id = uuid4()
        source = DataSource(
            source_id=source_id,
            name="test_source",
            source_type="csv",
            location="/path/to/data.csv",
        )

        assert source.source_id == source_id
        assert source.name == "test_source"
        assert source.source_type == "csv"
        assert source.location == "/path/to/data.csv"
        assert isinstance(source.metadata, dict)


class TestDataset:
    """Tests for Dataset entity."""

    def test_dataset_creation(self):
        """Test creating a Dataset."""
        dataset = Dataset(name="test_dataset")

        assert isinstance(dataset.dataset_id, UUID)
        assert dataset.name == "test_dataset"
        assert dataset.quality == DataQuality.UNKNOWN
        assert dataset.row_count == 0
        assert dataset.column_count == 0

    def test_update_quality(self):
        """Test updating dataset quality."""
        dataset = Dataset(name="test_dataset")
        original_time = dataset.updated_at

        dataset.update_quality(DataQuality.GOOD)

        assert dataset.quality == DataQuality.GOOD
        assert dataset.updated_at >= original_time


class TestModel:
    """Tests for Model entity."""

    def test_model_creation(self):
        """Test creating a Model."""
        model = Model(
            name="test_model",
            model_type="classification",
            algorithm="random_forest",
        )

        assert isinstance(model.model_id, UUID)
        assert model.name == "test_model"
        assert model.model_type == "classification"
        assert model.algorithm == "random_forest"
        assert model.version == "1.0.0"

    def test_update_metrics(self):
        """Test updating model metrics."""
        model = Model(name="test_model")
        metrics = {"accuracy": 0.95, "f1_score": 0.93}

        model.update_metrics(metrics)

        assert model.performance_metrics["accuracy"] == 0.95
        assert model.performance_metrics["f1_score"] == 0.93


class TestWorkflowExecution:
    """Tests for WorkflowExecution entity."""

    def test_workflow_execution_creation(self):
        """Test creating a WorkflowExecution."""
        execution = WorkflowExecution(
            workflow_name="test_workflow",
            total_steps=5,
        )

        assert isinstance(execution.execution_id, UUID)
        assert execution.workflow_name == "test_workflow"
        assert execution.status == ProcessingStatus.PENDING
        assert execution.total_steps == 5
        assert execution.steps_completed == 0

    def test_mark_completed(self):
        """Test marking execution as completed."""
        execution = WorkflowExecution(workflow_name="test_workflow")
        result = {"output": "success"}

        execution.mark_completed(result)

        assert execution.status == ProcessingStatus.COMPLETED
        assert execution.result == result
        assert execution.completed_at is not None

    def test_mark_failed(self):
        """Test marking execution as failed."""
        execution = WorkflowExecution(workflow_name="test_workflow")
        error_msg = "Something went wrong"

        execution.mark_failed(error_msg)

        assert execution.status == ProcessingStatus.FAILED
        assert execution.error == error_msg
        assert execution.completed_at is not None
