import sys
import os
import json
from datetime import datetime

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.file_ingestion import ingest_data
from validation.schema_validator import SchemaValidator
from preprocessing.feature_builder import FeatureBuilder
from eda.eda_report_generator import EdaReportGenerator
from utils.logging import Logger

def run_nexora_pipeline():
    logger = Logger.get_logger("MainPipeline")
    logger.info("Starting Nexora AI Phase-2 Pipeline")
    
    # Configuration
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "housing.csv")
    
    try:
        # 1. Ingestion
        print("\n[STEP 1] DATA INGESTION")
        data_bundle = ingest_data("csv", {"file_path": DATA_PATH})
        print(f"   Shape: {data_bundle.data.shape}")
        
        # 2. Validation
        print("\n[STEP 2] DATA VALIDATION")
        validator = SchemaValidator()
        data_bundle = validator.validate(data_bundle)
        print(f"   Health Score: {data_bundle.quality_report.get('health_score')}")
        
        # 3. Preprocessing
        print("\n[STEP 3] PREPROCESSING")
        preprocessor = FeatureBuilder()
        data_bundle = preprocessor.run(data_bundle)
        print("   Preprocessing complete.")
        
        # 4. EDA
        print("\n[STEP 4] EXPLORATORY DATA ANALYSIS")
        eda = EdaReportGenerator()
        data_bundle = eda.run(data_bundle)
        
        # -------------------------------------------------------------
        # PHASE-2: MACHINE LEARNING INTELLIGENCE ENGINE
        # -------------------------------------------------------------
        print("\n" + "="*50)
        print("PHASE-2: MACHINE LEARNING ENGINE STARTED")
        print("="*50)

        from ml_engine.problem_definition import ProblemDefiner
        from ml_engine.data_splitter import DataSplitter
        from ml_engine.model_trainer import ModelTrainer
        from ml_engine.feature_importance import FeatureImportance

        # 5. Problem Definition
        print("\n[STEP 5] PROBLEM DEFINITION")
        definer = ProblemDefiner()
        problem = definer.define_problem(data_bundle)
        print(f"   Task: {problem.task_type}")
        print(f"   Target: {problem.target}")
        print(f"   Features: {len(problem.features_used)} selected")

        # 6. Data Splitting
        print("\n[STEP 6] TRAIN-TEST SPLIT")
        splitter = DataSplitter()
        splits = splitter.split(data_bundle, problem)
        print(f"   Train Set: {splits['X_train'].shape}")
        print(f"   Test Set:  {splits['X_test'].shape}")

        # 7. Model Training & Selection
        print("\n[STEP 7] MODEL TRAINING & SELECTION")
        trainer = ModelTrainer()
        training_results = trainer.train_and_evaluate(
            splits["X_train"], splits["y_train"], 
            splits["X_test"], splits["y_test"], 
            problem.task_type
        )
        print(f"   Best Model: {training_results['best_model']}")
        print(f"   Reason: {training_results['reason']}")

        # 8. Feature Importance
        print("\n[STEP 8] FEATURE IMPORTANCE INTELLIGENCE")
        fi_extractor = FeatureImportance()
        top_features = fi_extractor.extract(training_results["all_results"], training_results["best_model"])
        
        # -------------------------------------------------------------
        # PHASE-3: DEEP LEARNING INTELLIGENCE ENGINE
        # -------------------------------------------------------------
        print("\n" + "="*50)
        print("PHASE-3: DEEP LEARNING ENGINE STARTED")
        print("="*50)

        from ml_engine.data_splitter import DataSplitter # Reuse for Val split
        from dl_engine.dl_trainer import DLTrainer
        from dl_engine.dl_vs_ml_analysis import ComparativeAnalysis

        # 9. Validation Split for DL
        print("\n[STEP 9] CREATING VALIDATION SET")
        # We split Training set into Train/Val
        from sklearn.model_selection import train_test_split
        X_train_dl, X_val_dl, y_train_dl, y_val_dl = train_test_split(
            splits["X_train"], splits["y_train"], 
            test_size=0.2, 
            random_state=42
        )
        print(f"   DL Train: {X_train_dl.shape}")
        print(f"   DL Val:   {X_val_dl.shape}")

        # 10. DL Training
        print("\n[STEP 10] NEURAL NETWORK TRAINING (ANN)")
        dl_trainer = DLTrainer()
        dl_results = dl_trainer.train_and_evaluate(
            X_train_dl, y_train_dl, 
            splits["X_test"], splits["y_test"], 
            X_val_dl, y_val_dl, 
            problem.task_type
        )
        ann_metrics = dl_results.get("ANN", {})
        print(f"   ANN R2: {ann_metrics.get('R2')}")

        # 11. ML vs DL Comparison
        print("\n[STEP 11] COMPARATIVE ANALYSIS")
        comparator = ComparativeAnalysis()
        final_verdict = comparator.compare(training_results, dl_results)
        print(f"   Decision: {final_verdict['final_decision']}")
        print(f"   Reason: {final_verdict['reason']}")

        # PRINT FINAL INSIGHTS
        print("\n" + "="*50)
        print("NEXORA AI ANALYST, ML & DL REPORT")
        print("="*50)
        
        print(f"\ndataset: {data_bundle.metadata.get('file_path')}")
        print(f"health_score: {data_bundle.quality_report.get('health_score')}\n")
        
        print("Data Insights:")
        for explanation in data_bundle.eda_insights["key_findings"][:3]:
            print(f" - {explanation}")
            
        print("\nModel Leaderboard:")
        print(f" 1. {training_results['best_model']} (ML): R2 = {training_results['all_results'][training_results['best_model']]['metrics']['R2']}")
        print(f" 2. ANN (Deep Learning): R2 = {ann_metrics.get('R2')}")
            
        print(f"\nFINAL SYSTEM RECOMMENDATION: {final_verdict['final_decision']}")
        print(f" -> {final_verdict['reason']}")
            
        print("\nPipeline Reasoning Logic:")
        for step in data_bundle.metadata["reasoning"]:
            print(f" [System] {step}")
            
        print("\n" + "="*50)
        print("PHASE-3 COMPLETE. READY FOR NLP ENGINE.")
        print("="*50)

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        print(f"\n[!] PIPELINE CRASHED: {e}")
        raise e

if __name__ == "__main__":
    run_nexora_pipeline()
