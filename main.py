import argparse
import sys
from nexora.core.config import Config
from nexora.core.exceptions import NexoraError
from nexora.orchestration.pipeline import NexoraPipeline

def main():
    Config.ensure_directories()
    
    parser = argparse.ArgumentParser(description="Nexora AI CLI")
    parser.add_argument("--source", required=True, help="Path to CSV data")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--task", choices=["regression", "classification"], required=True)
    parser.add_argument("--algo", choices=["rf", "linear", "logistic"], default="rf")
    
    args = parser.parse_args()
    
    pipeline = NexoraPipeline()
    try:
        results = pipeline.run(args.source, args.target, args.task, args.algo)
        print("\n" + "="*50)
        print(f"NEXORA AI REPORT (ID: {results['run_id']})")
        print("="*50)
        print(results['narrative'])
        print("="*50)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
