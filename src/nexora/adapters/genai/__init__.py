"""
GenAI adapters for generative AI and large language model integrations.
"""

from typing import Any, Optional

from nexora.application.ports import GenAIPort
from nexora.core.exceptions import GenAIException
from nexora.core.logger import get_logger
from nexora.domain.entities import Model, Explanation

logger = get_logger(__name__)


class LocalLLMAdapter(GenAIPort):
    """
    GenAI adapter for local language models.

    Integrates with locally hosted LLMs for text generation and insights.
    """

    def __init__(self, model_name: str = "llama", max_tokens: int = 512) -> None:
        """
        Initialize the local LLM adapter.

        Args:
            model_name: Name of the local LLM to use
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        logger.info(f"LocalLLMAdapter initialized with model={model_name}")

    def generate_text(
        self, prompt: str, context: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Generate text using a local LLM.

        Args:
            prompt: Input prompt
            context: Optional context for generation

        Returns:
            Generated text

        Raises:
            GenAIException: If generation fails
        """
        try:
            # In production, would interact with actual local LLM
            generated_text = (
                f"Generated response to: {prompt[:50]}... "
                f"[Simulated output from {self.model_name}]"
            )

            if context:
                generated_text += f"\nContext considered: {len(context)} items"

            logger.info(f"Generated text using {self.model_name}")
            return generated_text

        except Exception as e:
            raise GenAIException(
                f"Failed to generate text with {self.model_name}",
                details={"model_name": self.model_name, "prompt_length": len(prompt)},
                original_exception=e,
            )

    def generate_insights(
        self, model: Model, explanation: Explanation
    ) -> dict[str, Any]:
        """
        Generate insights from model and explanations using local LLM.

        Args:
            model: Model to generate insights for
            explanation: Explanation data

        Returns:
            Generated insights

        Raises:
            GenAIException: If insight generation fails
        """
        try:
            # In production, would generate actual insights using LLM
            insights = {
                "model_summary": f"The {model.model_type} model shows {len(explanation.feature_importance)} key features",
                "top_features": list(explanation.feature_importance.keys())[:5],
                "recommendations": [
                    "Consider feature engineering for top contributors",
                    "Monitor model performance on validation set",
                    "Evaluate model fairness and bias",
                ],
                "interpretation": f"Analysis generated using {self.model_name}",
            }

            logger.info(f"Generated insights for model {model.name} using {self.model_name}")
            return insights

        except Exception as e:
            raise GenAIException(
                f"Failed to generate insights with {self.model_name}",
                details={
                    "model_id": str(model.model_id),
                    "explanation_id": str(explanation.explanation_id),
                },
                original_exception=e,
            )


class PromptBasedGenAIAdapter(GenAIPort):
    """
    GenAI adapter using prompt engineering for structured outputs.

    Focuses on generating structured insights through carefully crafted prompts.
    """

    def __init__(self, temperature: float = 0.7, system_prompt: str = "") -> None:
        """
        Initialize the prompt-based GenAI adapter.

        Args:
            temperature: Sampling temperature for generation
            system_prompt: System-level instructions for the model
        """
        self.temperature = temperature
        self.system_prompt = system_prompt or "You are an AI assistant specialized in data science and machine learning."
        logger.info(f"PromptBasedGenAIAdapter initialized with temperature={temperature}")

    def generate_text(
        self, prompt: str, context: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Generate text using prompt engineering techniques.

        Args:
            prompt: Input prompt
            context: Optional context for generation

        Returns:
            Generated text

        Raises:
            GenAIException: If generation fails
        """
        try:
            # Build full prompt with system prompt and context
            full_prompt = f"{self.system_prompt}\n\n{prompt}"

            if context:
                full_prompt += f"\n\nContext:\n{self._format_context(context)}"

            # In production, would call actual LLM API
            generated_text = (
                f"Response generated with temperature={self.temperature}\n"
                f"Prompt: {prompt[:100]}..."
            )

            logger.info("Generated text using prompt-based approach")
            return generated_text

        except Exception as e:
            raise GenAIException(
                "Failed to generate text with prompt-based approach",
                details={"prompt_length": len(prompt), "temperature": self.temperature},
                original_exception=e,
            )

    def generate_insights(
        self, model: Model, explanation: Explanation
    ) -> dict[str, Any]:
        """
        Generate structured insights using prompt engineering.

        Args:
            model: Model to generate insights for
            explanation: Explanation data

        Returns:
            Generated insights

        Raises:
            GenAIException: If insight generation fails
        """
        try:
            # Craft structured prompt for insights
            prompt = self._build_insights_prompt(model, explanation)

            # In production, would generate actual insights
            insights = {
                "executive_summary": f"Model {model.name} analysis completed",
                "key_findings": [
                    f"Top feature: {list(explanation.feature_importance.keys())[0] if explanation.feature_importance else 'N/A'}",
                    f"Model type: {model.model_type}",
                    f"Performance: {model.performance_metrics.get('accuracy', 'N/A')}",
                ],
                "detailed_analysis": {
                    "feature_analysis": explanation.feature_importance,
                    "model_metrics": model.performance_metrics,
                },
                "actionable_recommendations": [
                    "Review top features for business relevance",
                    "Consider A/B testing before production deployment",
                    "Set up monitoring for model drift",
                ],
            }

            logger.info(f"Generated structured insights for model {model.name}")
            return insights

        except Exception as e:
            raise GenAIException(
                "Failed to generate insights with prompt-based approach",
                details={
                    "model_id": str(model.model_id),
                    "explanation_id": str(explanation.explanation_id),
                },
                original_exception=e,
            )

    def _format_context(self, context: dict[str, Any]) -> str:
        """Format context dictionary as readable text."""
        return "\n".join([f"- {k}: {v}" for k, v in context.items()])

    def _build_insights_prompt(self, model: Model, explanation: Explanation) -> str:
        """Build a structured prompt for generating insights."""
        return f"""
        Analyze the following machine learning model and provide insights:
        
        Model: {model.name}
        Type: {model.model_type}
        Algorithm: {model.algorithm}
        Metrics: {model.performance_metrics}
        
        Explanation Type: {explanation.explanation_type}
        Top Features: {list(explanation.feature_importance.keys())[:5]}
        
        Provide:
        1. Executive summary
        2. Key findings
        3. Detailed analysis
        4. Actionable recommendations
        """
