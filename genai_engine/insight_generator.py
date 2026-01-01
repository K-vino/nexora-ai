from jinja2 import Template
from typing import Dict, Any
from utils.logging import Logger
from genai_engine.prompt_templates import PromptTemplates
from datetime import datetime

class InsightGenerator:
    """
    Generates grounded narratives using Jinja2 templates and structured inputs.
    Strictly deterministic to prevent hallucination.
    """
    def __init__(self):
        self.logger = Logger.get_logger("InsightGenerator")
        
    def generate_executive_summary(self, 
                                   data_metadata: Dict[str, Any], 
                                   quality_report: Dict[str, Any], 
                                   model_results: Dict[str, Any],
                                   best_model_name: str,
                                   feature_importance: list) -> str:
        
        self.logger.info("Generating Executive Summary...")
        
        template_str = PromptTemplates.get_template("executive_summary")
        template = Template(template_str)
        
        # Extract metrics safely
        metrics = model_results["all_results"][best_model_name]["metrics"]
        r2 = metrics.get("R2", 0)
        
        # Logic for narrative
        perf_rating = "STRONG" if r2 > 0.8 else "MODERATE" if r2 > 0.5 else "WEAK"
        health_score = quality_report.get("health_score", 0)
        health_narrative = "Data is robust and clean." if health_score > 80 else "Data requires cleaning."
        
        context = {
            "project_name": "NEXORA AI",
            "execution_date": datetime.now().strftime("%Y-%m-%d"),
            "dataset_name": data_metadata.get("file_path", "Unknown"),
            "task_type": "Regression", # Dynamic in real app
            "target_variable": "median_house_value", # Dynamic
            "num_features": len(data_metadata.get("columns", [])),
            "health_score": health_score,
            "health_narrative": health_narrative,
            "best_model_name": best_model_name,
            "r2_score": round(r2, 4),
            "rmse": round(metrics.get("RMSE", 0), 2),
            "performance_rating": perf_rating,
            "top_feature": feature_importance[0]['feature'] if feature_importance else "None",
            "final_recommendation": f"Deploy {best_model_name} for predictive analysis.",
            "confidence_level": "HIGH" if r2 > 0.7 else "LOW"
        }
        
        return template.render(context)

    def generate_comparative_analysis(self, ml_best: str, ml_r2: float, dl_r2: float, decision: Dict[str, str]) -> str:
        self.logger.info("Generating Comparative Logic...")
        
        template_str = PromptTemplates.get_template("ml_vs_dl")
        template = Template(template_str)
        
        verdict = "Proven Stability matches Deep Learning potential." if abs(ml_r2 - dl_r2) < 0.05 else "Clear winner identified."
        
        context = {
            "ml_model": ml_best,
            "dl_model": "ANN (MLPRegressor)",
            "ml_r2": round(ml_r2, 4),
            "dl_r2": round(dl_r2, 4),
            "selected_model": decision['final_decision'],
            "reason_text": decision['reason'],
            "decision_narrative": verdict
        }
        
        return template.render(context)
        
    def generate_nlp_analysis(self, num_docs: int, topics: list, match: Dict[str, Any]) -> str:
        self.logger.info("Generating NLP Logic...")
        
        template_str = PromptTemplates.get_template("nlp_insight")
        template = Template(template_str)
        
        topic_strings = [", ".join(t['terms']) for t in topics]
        
        context = {
            "text_source": "Real Estate Descriptions",
            "doc_count": num_docs,
            "topics": topic_strings,
            "doc_id_1": "101",
            "doc_id_2": match['match_doc_id'] if match else "None",
            "similarity_score": match['score'] if match else "0.0"
        }
        
        return template.render(context)
