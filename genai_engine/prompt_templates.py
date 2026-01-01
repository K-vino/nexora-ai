from typing import Dict

# 1. Executive Summary Template
EXECUTIVE_SUMMARY_TEMPLATE = """
EXECUTIVE INTELLIGENCE SUMMARY
------------------------------
Project: {{ project_name }}
Date: {{ execution_date }}

OVERVIEW
The Nexora AI system analyzed the dataset '{{ dataset_name }}' to solve a {{ task_type }} problem. 
The goal was to predict '{{ target_variable }}' using {{ num_features }} features.

KEY OUTCOMES
1. Data Health: The dataset received a health score of {{ health_score }}/100. {{ health_narrative }}
2. Best Model: {{ best_model_name }} was selected as the optimal model.
3. Performance: It achieved an R2 score of {{ r2_score }} (RMSE: {{ rmse }}), indicates {{ performance_rating }} predictive power.
4. Top Driver: The most influential factor is '{{ top_feature }}'.

STRATEGIC RECOMMENDATION
{{ final_recommendation }}

CONFIDENCE SCORE: {{ confidence_level }}
"""

# 2. ML vs DL Comparison Template
ML_VS_DL_TEMPLATE = """
COMPARATIVE ARCHITECTURE ANALYSIS
---------------------------------
We evaluated two distinct intelligence architectures: Classical Machine Learning ({{ ml_model }}) and Deep Learning ({{ dl_model }}).

PERFORMANCE METRICS
- Classical ML ({{ ml_model }}): R2 = {{ ml_r2 }}
- Deep Learning ({{ dl_model }}): R2 = {{ dl_r2 }}

DECISION LOGIC
The system recommends **{{ selected_model }}**. 
Reasoning: {{ reason_text }}

VERDICT
{{ decision_narrative }}
"""

# 3. NLP Insight Template
NLP_INSIGHT_TEMPLATE = """
UNSTRUCTURED TEXT INTELLIGENCE
------------------------------
Source: {{ text_source }} ({{ doc_count }} documents)

THEMATIC ANALYSIS
Dominant themes detected in the text corpus:
{% for topic in topics %}
- Theme {{ loop.index }}: {{ topic }}
{% endfor %}

SIMILARITY SIGNAL
Complex pattern matching identified strong semantic links. 
Example: Document {{ doc_id_1 }} is {{ similarity_score }} similar to Document {{ doc_id_2 }}.
"""

class PromptTemplates:
    @staticmethod
    def get_template(name: str) -> str:
        templates = {
            "executive_summary": EXECUTIVE_SUMMARY_TEMPLATE,
            "ml_vs_dl": ML_VS_DL_TEMPLATE,
            "nlp_insight": NLP_INSIGHT_TEMPLATE
        }
        return templates.get(name, "")
