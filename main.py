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
    logger.info("Starting Nexora AI Phase-1 Pipeline: Data Intelligence Foundation")
    
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
        
        # PRINT FINAL INSIGHTS
        print("\n" + "="*50)
        print("NEXORA AI ANALYST REPORT")
        print("="*50)
        
        print(f"\ndataset: {data_bundle.metadata.get('file_path')}")
        print(f"health_score: {data_bundle.quality_report.get('health_score')}\n")
        
        print("Key Findings:")
        for explanation in data_bundle.eda_insights["key_findings"]:
            print(f" - {explanation}")
            
        print("\nRisks Identified:")
        for risk in data_bundle.eda_insights["risks"]:
            print(f" [!] {risk}")
            
        print("\nRecommended Next Steps:")
        for step in data_bundle.eda_insights["suggested_next_steps"]:
            print(f" -> {step}")
            
        print("\nPipeline Reasoning Logic:")
        for step in data_bundle.metadata["reasoning"]:
            print(f" [System] {step}")
            
        print("\n" + "="*50)
        print("PHASE-1 COMPLETE. STOPPING BEFORE MODELING.")
        print("="*50)

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        print(f"\n❌ PIPELINE CRASHED: {e}")
        raise e

if __name__ == "__main__":
    run_nexora_pipeline()
