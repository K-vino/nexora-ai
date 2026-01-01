from genai_engine.insight_generator import InsightGenerator
from genai_engine.report_writer import ReportWriter

print("Testing InsightGenerator...")
genai = InsightGenerator()

# Mock Data
data_meta = {"file_path": "test.csv", "columns": ["A", "B"]}
quality = {"health_score": 95}
results = {
    "all_results": {
        "Linear Regression": {"metrics": {"R2": 0.85, "RMSE": 0.1}}
    }
}
feat_imp = [{"feature": "A", "importance": 0.5}]

# A. Exec Summary
print("Generating Executive Summary...")
summary = genai.generate_executive_summary(data_meta, quality, results, "Linear Regression", feat_imp)
print(summary)

# B. Comp Analysis
print("Generating Comp Analysis...")
comp = genai.generate_comparative_analysis("Linear Regression", 0.85, 0.82, {"final_decision": "ML", "reason": "Better"})
print(comp)

# C. NLP
print("Generating NLP...")
nlp = genai.generate_nlp_analysis(10, [{"terms": ["a", "b"]}], {"match_doc_id": "102", "score": 0.9})
print(nlp)

print("Testing ReportWriter...")
writer = ReportWriter()
path = writer.save_report(summary + comp + nlp, "test")
print(f"Saved to {path}")
