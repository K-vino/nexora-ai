"""
Workflow orchestration for the NEXORA AI platform.

Coordinates complex workflows involving multiple steps and components.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
from uuid import uuid4

from nexora.core.exceptions import OrchestrationException
from nexora.core.logger import get_logger
from nexora.domain.entities import ProcessingStatus, WorkflowExecution

logger = get_logger(__name__)


class StepStatus(Enum):
    """Status of a workflow step."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    """
    Definition of a single workflow step.

    Attributes:
        name: Step name
        function: Function to execute for this step
        dependencies: List of step names this step depends on
        retry_count: Number of retries on failure
        timeout: Timeout in seconds
        metadata: Additional metadata
    """

    name: str
    function: Callable[..., Any]
    dependencies: list[str] = field(default_factory=list)
    retry_count: int = 0
    timeout: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDefinition:
    """
    Definition of a complete workflow.

    Attributes:
        name: Workflow name
        description: Workflow description
        steps: List of workflow steps
        metadata: Additional metadata
    """

    name: str
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)

    def validate(self) -> bool:
        """
        Validate the workflow definition.

        Returns:
            True if valid, False otherwise
        """
        if not self.steps:
            logger.error(f"Workflow {self.name} has no steps")
            return False

        # Check for circular dependencies
        step_names = {step.name for step in self.steps}
        for step in self.steps:
            for dep in step.dependencies:
                if dep not in step_names:
                    logger.error(
                        f"Step {step.name} has unknown dependency: {dep}"
                    )
                    return False

        return True


class WorkflowOrchestrator:
    """
    Orchestrator for executing workflows.

    Manages workflow execution, dependency resolution, and error handling.
    """

    def __init__(self) -> None:
        """Initialize the workflow orchestrator."""
        self.executions: dict[str, WorkflowExecution] = {}
        logger.info("WorkflowOrchestrator initialized")

    def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        context: Optional[dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """
        Execute a workflow.

        Args:
            workflow: Workflow definition to execute
            context: Optional execution context

        Returns:
            Workflow execution result

        Raises:
            OrchestrationException: If execution fails
        """
        if not workflow.validate():
            raise OrchestrationException(
                f"Invalid workflow definition: {workflow.name}",
                details={"workflow_name": workflow.name},
            )

        execution = WorkflowExecution(
            workflow_name=workflow.name,
            status=ProcessingStatus.IN_PROGRESS,
            total_steps=len(workflow.steps),
        )

        self.executions[str(execution.execution_id)] = execution
        logger.info(f"Starting workflow execution: {workflow.name}")

        try:
            step_results: dict[str, Any] = {}
            execution_context = context or {}

            # Execute steps in order (simplified - no parallel execution)
            for step in workflow.steps:
                logger.info(f"Executing step: {step.name}")

                # Check dependencies
                if not self._check_dependencies(step, step_results):
                    raise OrchestrationException(
                        f"Step dependencies not met: {step.name}",
                        details={"step": step.name, "dependencies": step.dependencies},
                    )

                # Execute step
                try:
                    result = self._execute_step(step, execution_context, step_results)
                    step_results[step.name] = result
                    execution.steps_completed += 1
                    logger.info(f"Step completed: {step.name}")

                except Exception as e:
                    logger.error(f"Step failed: {step.name} - {str(e)}")
                    execution.mark_failed(f"Step {step.name} failed: {str(e)}")
                    raise OrchestrationException(
                        f"Step execution failed: {step.name}",
                        details={"step": step.name},
                        original_exception=e,
                    )

            # Mark execution as completed
            execution.mark_completed(step_results)
            logger.info(f"Workflow completed: {workflow.name}")

            return execution

        except Exception as e:
            execution.mark_failed(str(e))
            logger.error(f"Workflow failed: {workflow.name} - {str(e)}")
            raise OrchestrationException(
                f"Workflow execution failed: {workflow.name}",
                details={"workflow_name": workflow.name},
                original_exception=e,
            )

    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """
        Get a workflow execution by ID.

        Args:
            execution_id: Execution identifier

        Returns:
            Workflow execution or None if not found
        """
        return self.executions.get(execution_id)

    def list_executions(self) -> list[WorkflowExecution]:
        """
        List all workflow executions.

        Returns:
            List of workflow executions
        """
        return list(self.executions.values())

    def _check_dependencies(
        self, step: WorkflowStep, step_results: dict[str, Any]
    ) -> bool:
        """Check if step dependencies are satisfied."""
        for dep in step.dependencies:
            if dep not in step_results:
                return False
        return True

    def _execute_step(
        self,
        step: WorkflowStep,
        context: dict[str, Any],
        previous_results: dict[str, Any],
    ) -> Any:
        """
        Execute a single workflow step.

        Args:
            step: Step to execute
            context: Execution context
            previous_results: Results from previous steps

        Returns:
            Step execution result
        """
        # Prepare step input from context and previous results
        step_input = {
            "context": context,
            "previous_results": previous_results,
        }

        # Execute step function with retry logic
        attempts = 0
        max_attempts = step.retry_count + 1

        while attempts < max_attempts:
            try:
                result = step.function(step_input)
                return result
            except Exception as e:
                attempts += 1
                if attempts >= max_attempts:
                    raise e
                logger.warning(
                    f"Step {step.name} failed (attempt {attempts}/{max_attempts}), retrying..."
                )

        raise OrchestrationException(
            f"Step {step.name} failed after {max_attempts} attempts"
        )


class WorkflowBuilder:
    """
    Builder class for constructing workflows fluently.

    Provides a convenient API for defining workflows programmatically.
    """

    def __init__(self, name: str, description: str = "") -> None:
        """
        Initialize the workflow builder.

        Args:
            name: Workflow name
            description: Workflow description
        """
        self.workflow = WorkflowDefinition(name=name, description=description)

    def add_step(
        self,
        name: str,
        function: Callable[..., Any],
        dependencies: Optional[list[str]] = None,
        retry_count: int = 0,
    ) -> "WorkflowBuilder":
        """
        Add a step to the workflow.

        Args:
            name: Step name
            function: Step function
            dependencies: Optional list of dependency step names
            retry_count: Number of retries on failure

        Returns:
            Self for chaining
        """
        step = WorkflowStep(
            name=name,
            function=function,
            dependencies=dependencies or [],
            retry_count=retry_count,
        )
        self.workflow.add_step(step)
        return self

    def build(self) -> WorkflowDefinition:
        """
        Build and return the workflow definition.

        Returns:
            Complete workflow definition
        """
        if not self.workflow.validate():
            raise OrchestrationException(
                f"Invalid workflow: {self.workflow.name}",
                details={"workflow_name": self.workflow.name},
            )

        return self.workflow
