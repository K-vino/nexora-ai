# NEXORA AI

> A modular, local-first Enterprise Intelligence Platform that unifies data ingestion, validation, feature engineering, machine learning, explainable AI, and GenAI-driven narrative reporting into a single production-grade Python system.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🏗️ Architecture

NEXORA AI follows a **Hexagonal Architecture** (Ports and Adapters) pattern, ensuring clean separation of concerns, testability, and maintainability.

```
src/nexora/
├── core/                    # Core abstractions, exceptions, logging
│   ├── base.py             # Abstract base classes
│   ├── exceptions.py       # Custom exception hierarchy
│   └── logger.py           # Logging configuration
├── domain/                  # Business entities and domain logic
│   └── entities.py         # Domain entities (Dataset, Model, etc.)
├── application/            # Use cases and port definitions
│   ├── ports.py           # Port interfaces
│   └── use_cases.py       # Business use cases
├── adapters/              # Implementations of ports
│   ├── ingestion/         # Data ingestion adapters
│   ├── validation/        # Data validation adapters
│   ├── feature_engineering/ # Feature engineering adapters
│   ├── modeling/          # ML modeling adapters
│   ├── explainability/    # Model explanation adapters
│   ├── genai/            # GenAI integration adapters
│   └── reporting/         # Report generation adapters
├── infrastructure/        # Configuration and utilities
│   └── config.py         # Configuration management
└── orchestration/         # Workflow coordination
    └── workflow_orchestrator.py
```

## ✨ Features

### Core Capabilities
- **🔌 Hexagonal Architecture**: Clean separation between business logic and infrastructure
- **📊 Data Ingestion**: Support for multiple data sources (files, databases)
- **✅ Data Validation**: Quality assessment and schema validation
- **🔧 Feature Engineering**: Standard and time-series feature transformations
- **🤖 Machine Learning**: Support for scikit-learn and deep learning models
- **🔍 Explainability**: SHAP, LIME, and permutation importance
- **🧠 GenAI Integration**: Local LLM and prompt-based generation
- **📝 Reporting**: Markdown, HTML, and JSON report generation
- **⚙️ Workflow Orchestration**: Multi-step pipeline coordination

### Design Principles
- **Strict OOP Design**: Abstract base classes and interfaces throughout
- **Type Hints**: Complete type annotations for all functions and methods
- **Custom Exceptions**: Comprehensive exception hierarchy with context
- **Structured Logging**: Consistent logging across all modules
- **No External Cloud**: Fully local-first architecture
- **Interview-Ready**: Production-grade code structure and patterns

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/K-vino/nexora-ai.git
cd nexora-ai

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```python
from nexora.adapters.ingestion import FileIngestionAdapter
from nexora.adapters.validation import StandardValidationAdapter
from nexora.application.use_cases import IngestDataUseCase

# Initialize adapters
ingestion = FileIngestionAdapter()
validation = StandardValidationAdapter()

# Create use case
ingest_use_case = IngestDataUseCase(ingestion, validation)

# Execute
dataset = ingest_use_case.execute("data.csv", "csv")
print(f"Ingested dataset: {dataset.name}")
```

### Complete Workflow Example

```python
from nexora.orchestration import WorkflowBuilder, WorkflowOrchestrator

# Build workflow
workflow = (
    WorkflowBuilder("ml_pipeline", "Complete ML pipeline")
    .add_step("ingest", ingest_function)
    .add_step("validate", validate_function, dependencies=["ingest"])
    .add_step("train", train_function, dependencies=["validate"])
    .add_step("explain", explain_function, dependencies=["train"])
    .add_step("report", report_function, dependencies=["explain"])
    .build()
)

# Execute workflow
orchestrator = WorkflowOrchestrator()
execution = orchestrator.execute_workflow(workflow)
print(f"Status: {execution.status.value}")
```

See `example_usage.py` for a complete demonstration.

## 📦 Project Structure

```
nexora-ai/
├── src/nexora/              # Main package
│   ├── core/               # Core abstractions
│   ├── domain/             # Domain entities
│   ├── application/        # Use cases and ports
│   ├── adapters/          # Adapter implementations
│   ├── infrastructure/     # Configuration
│   └── orchestration/      # Workflow management
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/        # Integration tests
├── example_usage.py        # Usage examples
├── pyproject.toml         # Project configuration
├── setup.py               # Setup script
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nexora --cov-report=html

# Run specific test file
pytest tests/unit/core/test_exceptions.py
```

## 🛠️ Development

### Code Quality Tools

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type checking with mypy
mypy src/
```

### Adding New Adapters

1. Define the port interface in `application/ports.py`
2. Implement the adapter in the appropriate `adapters/` subdirectory
3. Follow existing patterns for error handling and logging
4. Add comprehensive tests

Example:

```python
# In application/ports.py
class MyCustomPort(ABC):
    @abstractmethod
    def my_method(self, data: Input) -> Output:
        pass

# In adapters/my_custom/
class MyCustomAdapter(MyCustomPort):
    def my_method(self, data: Input) -> Output:
        # Implementation
        pass
```

## 📚 Documentation

### Key Concepts

**Ports**: Interfaces that define contracts between the application and external systems
- `DataIngestionPort`: Interface for data ingestion
- `DataValidationPort`: Interface for validation
- `ModelingPort`: Interface for ML operations
- And more...

**Adapters**: Concrete implementations of ports
- `FileIngestionAdapter`: Ingest from local files
- `SklearnModelingAdapter`: Scikit-learn models
- `SHAPExplainabilityAdapter`: SHAP explanations
- And more...

**Use Cases**: Orchestrate business operations
- `IngestDataUseCase`: Ingest and validate data
- `TrainModelUseCase`: Engineer features and train model
- `ExplainModelUseCase`: Generate explanations and insights
- `GenerateReportUseCase`: Create comprehensive reports

**Entities**: Domain objects
- `Dataset`: Represents a dataset
- `Model`: Represents a trained model
- `Explanation`: Model explanation
- `Report`: Generated report
- `WorkflowExecution`: Workflow execution state

## 🎯 Use Cases

### Data Science Pipeline
1. Ingest data from various sources
2. Validate and assess data quality
3. Engineer features
4. Train and evaluate models
5. Generate explanations
6. Create narrative reports

### Model Explainability
1. Load trained model
2. Generate SHAP/LIME explanations
3. Use GenAI to create insights
4. Export comprehensive reports

### Workflow Automation
1. Define multi-step workflows
2. Manage dependencies between steps
3. Handle failures and retries
4. Track execution status

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow the existing architecture patterns
2. Add type hints to all functions
3. Write comprehensive tests
4. Update documentation
5. Follow the code style (Black + Ruff)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hexagonal Architecture pattern by Alistair Cockburn
- Clean Architecture principles by Robert C. Martin
- Domain-Driven Design concepts by Eric Evans

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a scaffold/framework. For production use, implement actual data processing, ML algorithms, and GenAI integrations according to your specific requirements.
