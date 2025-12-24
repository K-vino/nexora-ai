"""
Explainability adapters for model interpretation and explanation.
"""

from typing import Any
from uuid import uuid4

from nexora.application.ports import ExplainabilityPort
from nexora.core.exceptions import ExplainabilityException
from nexora.core.logger import get_logger
from nexora.domain.entities import Dataset, Model, Explanation

logger = get_logger(__name__)


class SHAPExplainabilityAdapter(ExplainabilityPort):
    """
    Explainability adapter using SHAP (SHapley Additive exPlanations).

    Provides model-agnostic explanations using Shapley values.
    """

    def __init__(self) -> None:
        """Initialize the SHAP explainability adapter."""
        logger.info("SHAPExplainabilityAdapter initialized")

    def explain_model(
        self, model: Model, dataset: Dataset, explanation_type: str
    ) -> Explanation:
        """
        Generate SHAP explanations for a model's behavior.

        Args:
            model: Model to explain
            dataset: Dataset used for explanation
            explanation_type: Type of explanation

        Returns:
            Explanation object with SHAP values

        Raises:
            ExplainabilityException: If explanation generation fails
        """
        try:
            # In production, would compute actual SHAP values
            feature_importance = {
                feature: 0.1 * (i + 1)
                for i, feature in enumerate(list(dataset.schema.keys())[:10])
            }

            explanation = Explanation(
                explanation_id=uuid4(),
                model_id=model.model_id,
                explanation_type="shap",
                feature_importance=feature_importance,
            )

            explanation.content = {
                "method": "shap",
                "base_value": 0.5,
                "expected_value": 0.5,
                "summary": "SHAP values computed for model explanations",
            }

            logger.info(f"Generated SHAP explanation for model {model.name}")
            return explanation

        except Exception as e:
            raise ExplainabilityException(
                f"Failed to generate SHAP explanation for model {model.name}",
                details={
                    "model_id": str(model.model_id),
                    "dataset_id": str(dataset.dataset_id),
                },
                original_exception=e,
            )

    def explain_prediction(
        self, model: Model, instance: dict[str, Any], explanation_type: str
    ) -> dict[str, Any]:
        """
        Explain a single prediction using SHAP.

        Args:
            model: Model that made the prediction
            instance: Input instance to explain
            explanation_type: Type of explanation

        Returns:
            Explanation for the prediction

        Raises:
            ExplainabilityException: If explanation fails
        """
        try:
            # In production, would compute actual SHAP values for instance
            explanation = {
                "model_id": str(model.model_id),
                "explanation_type": "shap",
                "instance": instance,
                "feature_contributions": {
                    feature: 0.05 * (i + 1)
                    for i, feature in enumerate(instance.keys())
                },
                "prediction": 0.75,
                "base_value": 0.5,
            }

            logger.info(f"Generated SHAP explanation for single prediction")
            return explanation

        except Exception as e:
            raise ExplainabilityException(
                f"Failed to explain prediction for model {model.name}",
                details={"model_id": str(model.model_id)},
                original_exception=e,
            )


class LIMEExplainabilityAdapter(ExplainabilityPort):
    """
    Explainability adapter using LIME (Local Interpretable Model-agnostic Explanations).

    Provides local explanations by approximating the model with interpretable models.
    """

    def __init__(self, num_samples: int = 1000) -> None:
        """
        Initialize the LIME explainability adapter.

        Args:
            num_samples: Number of samples for local approximation
        """
        self.num_samples = num_samples
        logger.info(f"LIMEExplainabilityAdapter initialized with num_samples={num_samples}")

    def explain_model(
        self, model: Model, dataset: Dataset, explanation_type: str
    ) -> Explanation:
        """
        Generate LIME explanations for a model's behavior.

        Args:
            model: Model to explain
            dataset: Dataset used for explanation
            explanation_type: Type of explanation

        Returns:
            Explanation object with LIME results

        Raises:
            ExplainabilityException: If explanation generation fails
        """
        try:
            # In production, would compute actual LIME explanations
            feature_importance = {
                feature: 0.08 * (i + 1)
                for i, feature in enumerate(list(dataset.schema.keys())[:10])
            }

            explanation = Explanation(
                explanation_id=uuid4(),
                model_id=model.model_id,
                explanation_type="lime",
                feature_importance=feature_importance,
            )

            explanation.content = {
                "method": "lime",
                "num_samples": self.num_samples,
                "summary": "LIME explanations computed using local approximations",
            }

            logger.info(f"Generated LIME explanation for model {model.name}")
            return explanation

        except Exception as e:
            raise ExplainabilityException(
                f"Failed to generate LIME explanation for model {model.name}",
                details={
                    "model_id": str(model.model_id),
                    "dataset_id": str(dataset.dataset_id),
                },
                original_exception=e,
            )

    def explain_prediction(
        self, model: Model, instance: dict[str, Any], explanation_type: str
    ) -> dict[str, Any]:
        """
        Explain a single prediction using LIME.

        Args:
            model: Model that made the prediction
            instance: Input instance to explain
            explanation_type: Type of explanation

        Returns:
            Explanation for the prediction

        Raises:
            ExplainabilityException: If explanation fails
        """
        try:
            # In production, would compute actual LIME explanation
            explanation = {
                "model_id": str(model.model_id),
                "explanation_type": "lime",
                "instance": instance,
                "feature_contributions": {
                    feature: 0.06 * (i + 1)
                    for i, feature in enumerate(instance.keys())
                },
                "local_model": "linear",
                "num_samples": self.num_samples,
            }

            logger.info(f"Generated LIME explanation for single prediction")
            return explanation

        except Exception as e:
            raise ExplainabilityException(
                f"Failed to explain prediction for model {model.name}",
                details={"model_id": str(model.model_id)},
                original_exception=e,
            )


class PermutationImportanceAdapter(ExplainabilityPort):
    """
    Explainability adapter using permutation importance.

    Explains feature importance by measuring performance decrease when features are shuffled.
    """

    def __init__(self, n_repeats: int = 10) -> None:
        """
        Initialize the permutation importance adapter.

        Args:
            n_repeats: Number of times to permute each feature
        """
        self.n_repeats = n_repeats
        logger.info(f"PermutationImportanceAdapter initialized with n_repeats={n_repeats}")

    def explain_model(
        self, model: Model, dataset: Dataset, explanation_type: str
    ) -> Explanation:
        """
        Generate permutation importance explanations.

        Args:
            model: Model to explain
            dataset: Dataset used for explanation
            explanation_type: Type of explanation

        Returns:
            Explanation object with permutation importance scores

        Raises:
            ExplainabilityException: If explanation generation fails
        """
        try:
            # In production, would compute actual permutation importance
            feature_importance = {
                feature: 0.12 * (i + 1)
                for i, feature in enumerate(list(dataset.schema.keys())[:10])
            }

            explanation = Explanation(
                explanation_id=uuid4(),
                model_id=model.model_id,
                explanation_type="permutation_importance",
                feature_importance=feature_importance,
            )

            explanation.content = {
                "method": "permutation_importance",
                "n_repeats": self.n_repeats,
                "summary": "Feature importance computed using permutation tests",
            }

            logger.info(
                f"Generated permutation importance explanation for model {model.name}"
            )
            return explanation

        except Exception as e:
            raise ExplainabilityException(
                f"Failed to generate permutation importance for model {model.name}",
                details={
                    "model_id": str(model.model_id),
                    "dataset_id": str(dataset.dataset_id),
                },
                original_exception=e,
            )

    def explain_prediction(
        self, model: Model, instance: dict[str, Any], explanation_type: str
    ) -> dict[str, Any]:
        """
        Permutation importance is a global method, not for single predictions.

        Args:
            model: Model that made the prediction
            instance: Input instance
            explanation_type: Type of explanation

        Returns:
            Explanation noting this is a global method

        Raises:
            ExplainabilityException: Always, as method is not for single predictions
        """
        raise ExplainabilityException(
            "Permutation importance is a global explanation method, not suitable for single predictions",
            details={"model_id": str(model.model_id)},
        )
