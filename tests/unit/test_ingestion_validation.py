import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from nexora.ingestion.csv_connector import CSVConnector
from nexora.validation.anomaly_detector import AnomalyDetector

@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame({
        'A': range(100),
        'B': np.random.randn(100),
        'C': ['cat', 'dog'] * 50
    })
    path = tmp_path / "test.csv"
    df.to_csv(path, index=False)
    return str(path)

@pytest.fixture
def anomalous_df():
    df = pd.DataFrame({
        'val': [1, 2, 3, 1, 2, 100, 1, 2, 3, -50]
    })
    return df

def test_csv_metadata(sample_csv):
    """Test metadata extraction from CSV."""
    connector = CSVConnector()
    metadata = connector.get_metadata(sample_csv)
    
    assert "columns" in metadata
    assert metadata["columns"] == ['A', 'B', 'C']
    assert "dtypes" in metadata
    assert "file_size_mb" in metadata

def test_anomaly_summary(anomalous_df):
    """Test anomaly summary generation."""
    detector = AnomalyDetector(factor=1.5)
    
    # Test with IQR
    outliers_iqr = detector.detect_outliers(anomalous_df)
    summary_iqr = detector.summarize_anomalies(anomalous_df, outliers_iqr)
    
    assert summary_iqr["total_rows"] == 10
    assert summary_iqr["anomaly_count"] == 2 # 100 and -50 likely outliers
    assert summary_iqr["contamination_ratio"] == 0.2
    
def test_isolation_forest():
    """Test Isolation Forest execution."""
    df = pd.DataFrame(np.random.randn(100, 2), columns=['A', 'B'])
    # Add outlier
    df.iloc[0] = [100, 100]
    
    detector = AnomalyDetector()
    results = detector.detect_anomalies_isolation_forest(df)
    
    assert results.sum() > 0
    assert results.iloc[0] == True
