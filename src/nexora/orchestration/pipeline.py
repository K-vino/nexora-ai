import sys
import uuid
from typing import Optional, Dict, Any
from nexora.core.config import Config
from nexora.core.logger import Logger
from nexora.core.exceptions import NexoraError
from nexora.ingestion.csv_connector import CSVConnector
from nexora.validation.schema_validator import SchemaValidator
from nexora.feature_engineering.auto_imputer import AutoImputer
from nexora.validation.anomaly_detector import AnomalyDetector
from nexora.modeling.regression import RandomForestRegressionStrategy, LinearRegressionStrategy
from nexora.modeling.classification import RandomForestClassificationStrategy, LogisticRegressionStrategy
from nexora.modeling.evaluator import ModelEvaluator
from nexora.explainability.shap_wrapper import SHAPWrapper
from nexora.genai.mock_llm_adapter import MockLLMAdapter
from nexora.reporting.report_generator import ReportGenerator

from sklearn.model_selection import train_test_split
import pandas as pd

class NexoraPipeline:
    """
    Main Orchestrator for the Nexora AI System.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("Orchestrator")
        self.connector = CSVConnector()
        self.validator = SchemaValidator()
        self.anomaly_detector = AnomalyDetector()
        self.imputer = AutoImputer()
        self.evaluator = ModelEvaluator()
        self.explainer = SHAPWrapper()
        self.genai = MockLLMAdapter()
        self.reporter = ReportGenerator()
        
    def _get_model_strategy(self, task: str, algo: str):
        if task == "regression":
            return LinearRegressionStrategy() if algo == "linear" else RandomForestRegressionStrategy()
        elif task == "classification":
            return LogisticRegressionStrategy() if algo == "logistic" else RandomForestClassificationStrategy()
        else:
            raise ValueError(f"Unknown task: {task}")

    def run(self, source: str, target: str, task: str, algo: str = "rf") -> Dict[str, Any]:
        """
        Executes the pipeline and returns results.
        Raises NexoraError on known failures.
        """
        run_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Starting Nexora Pipeline [Run ID: {run_id}]")
        
        try:
            # 1. Ingestion
            df = self.connector.load_data(source)
            
            # 2. Validation
            self.validator.validate(df)
            
            # Advanced Anomaly Detection (Isolation Forest)
            anomalies = self.anomaly_detector.detect_anomalies_isolation_forest(df)
            if anomalies.any():
                self.logger.warning(f"Isolation Forest detected {anomalies.sum()} anomalies. Proceeding with caution.")
                # In a real system, we might drop them or flag them.
            
            if target not in df.columns:
                raise ValueError(f"Target column '{target}' not found in dataset.")
                
            # 3. Splitting (Simple Train/Test)
            X = df.drop(columns=[target])
            y = df[target]
            
            # 4. Feature Engineering (Imputation)
            # fit_transform on whole X for simplicity of current constraints
            self.imputer.fit(X)
            X_clean = self.imputer.transform(X)
            
            # OHE for categoricals (Minimal handling for demo)
            X_clean = pd.get_dummies(X_clean, drop_first=True)
            
            X_train, X_test, y_train, y_test = train_test_split(X_clean, y, test_size=0.2, random_state=42)
            
            # 5. Modeling
            strategy = self._get_model_strategy(task, algo)
            model = strategy.train(X_train, y_train)
            predictions = strategy.predict(X_test)
            
            # 6. Evaluation
            metrics = self.evaluator.evaluate(y_test, predictions, task)
            
            # 7. Explainability
            importance = self.explainer.explain_global(model, X_train)
            
            # 8. GenAI Narrative
            context = {"metrics": metrics, "importance": importance, "anomalies_detected": int(anomalies.sum())}
            narrative = self.genai.generate_narrative(context)
            
            # 9. Reporting
            report_data = {
                "run_id": run_id,
                "config": {"source": source, "target": target, "task": task, "algo": algo},
                "metrics": metrics,
                "importance": importance,
                "narrative": narrative,
                "anomalies_detected": int(anomalies.sum())
            }
            output_path = self.reporter.save_report(run_id, report_data)
            html_path = self.reporter.generate_html_report(run_id, report_data)
            
            self.logger.info(f"Pipeline finished successfully. JSON: {output_path}, HTML: {html_path}")
            
            return {
                "run_id": run_id,
                "status": "success",
                "metrics": metrics,
                "importance": importance,
                "narrative": narrative,
                "report_path": str(output_path),
                "html_report_path": str(html_path) if html_path else None
            }
            
        except NexoraError as e:
            self.logger.error(f"Pipeline logic failed: {e}")
            raise e
        except Exception as e:
            self.logger.critical(f"System crash: {e}")
            raise e
