import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from nexora.orchestration.pipeline import NexoraPipeline
from utils.config import Config

@pytest.fixture
def sample_data(tmp_path):
    # Create sophisticated dummy data
    df = pd.DataFrame({
        'feature_num': np.random.randn(50),
        'feature_cat': ['A', 'B', 'A', 'C', 'B'] * 10,
        'target': np.random.randn(50) # Regression target
    })
    # Add some anomalies
    df.loc[0, 'feature_num'] = 100
    
    path = tmp_path / "integration_test.csv"
    df.to_csv(path, index=False)
    return str(path)

def test_pipeline_end_to_end_regression(sample_data):
    pipeline = NexoraPipeline()
    
    # 1. Run Regression
    result = pipeline.run(
        source=sample_data,
        target='target',
        task='regression',
        algo='rf'
    )
    
    assert result['status'] == 'success'
    assert 'rmse' in result['metrics']
    assert 'mae' in result['metrics']
    assert result['anomalies_summary']['anomaly_count'] > 0
    assert result['narrative'] is not None
    assert Path(result['report_path']).exists()
    assert Path(result['html_report_path']).exists()

def test_pipeline_classification(tmp_path):
    df = pd.DataFrame({
        'f1': np.random.randn(50),
        'label': [0, 1] * 25
    })
    path = tmp_path / "clf_test.csv"
    df.to_csv(path, index=False)
    
    pipeline = NexoraPipeline()
    result = pipeline.run(
        source=str(path),
        target='label',
        task='classification',
        algo='logistic'
    )
    
    assert result['status'] == 'success'
    assert 'accuracy' in result['metrics']
    assert 'precision' in result['metrics']
