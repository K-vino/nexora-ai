# NEXORA AI

**Nexora AI** is a modular, local-first **Enterprise Intelligence Platform** that unifies data ingestion, validation, feature engineering, machine learning, explainable AI, and GenAI-driven narrative reporting into a single production-grade Python system.

Designed for flexibility and scalability, Nexora AI enables data teams to build robust end-to-end ML pipelines with built-in interpretability and automated reporting.

## Key Features

*   **Modular Architecture**: Clean separation of concerns with dedicated modules for Ingestion, Validation, Feature Engineering, Modeling, Explainability, and Reporting.
*   **Data Ingestion**: Robust handling of data sources (CSV) with extensible support for others.
*   **Automated Validation**: Schema and data quality checks to ensure reliable inputs.
*   **Feature Engineering**: Automated preprocessing and feature extraction.
*   **Model Training**:
    *   **Tasks**: Regression and Classification.
    *   **Algorithms**: Random Forest, Linear Regression, Logistic Regression.
*   **Explainable AI (XAI)**: Integrated insights into model predictions to ensure transparency.
*   **GenAI Reporting**: Generates narrative reports explaining analysis results using Generative AI.
*   **Web Dashboard**: A FastAPI-based web interface and API for interacting with the platform.

## Installation

### Prerequisites
*   Python 3.8+
*   pip

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/nexora-ai.git
    cd nexora-ai
    ```

2.  Install the package in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

### Command Line Interface (CLI)

You can run the full pipeline directly from the command line using `main.py`.

**Arguments:**
*   `--source`: Path to the input CSV data file.
*   `--target`: Name of the target column for prediction.
*   `--task`: Task type (`regression` or `classification`).
*   `--algo`: Algorithm to use (`rf` [Random Forest], `linear` [Linear Regression], `logistic` [Logistic Regression]). Default is `rf`.

**Example:**
Run a classification task using Random Forest on a sample dataset:

```bash
python main.py --source data/sample_data.csv --target churn --task classification --algo rf
```

### Web Interface & API

Nexora AI includes a modern web dashboard and REST API built with FastAPI.

To start the server:

```bash
uvicorn nexora.web.api:app --reload
```

*   **Dashboard**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
*   **API Docs**: Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API documentation.

## Project Structure

The source code is organized clearly in `src/nexora`:

*   `core/`: Core configurations and exception handling.
*   `ingestion/`: Data loading and parsing.
*   `validation/`: Data quality and schema validation.
*   `feature_engineering/`: Data transformation and feature creation.
*   `modeling/`: Model training and evaluation logic.
*   `explainability/`: Model interpretation tools.
*   `genai/`: Narrative generation components.
*   `reporting/`: Report generation and formatting.
*   `orchestration/`: Pipeline coordination.
*   `web/`: Web application and API endpoints.

## Development

 To run the test suite:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
