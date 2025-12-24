from fastapi.testclient import TestClient
from nexora.web.api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("nexora.web.endpoints.NexoraPipeline")
def test_run_pipeline_endpoint(MockPipeline):
    # Mock return value
    mock_instance = MockPipeline.return_value
    mock_instance.run.return_value = {
        "run_id": "test_123",
        "status": "success",
        "metrics": {"r2": 0.95},
        "narrative": "Excellent fit.",
        "importance": {"DistanceToCity": 0.8},
        "report_path": "/tmp/report.json"
    }

    response = client.post("/api/run", json={
        "source_path": "data/housing.csv",
        "target_column": "Price",
        "task": "regression",
        "algorithm": "rf"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == "test_123"
    assert data["metrics"]["r2"] == 0.95

def test_root_ui_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "NEXORA AI" in response.text
