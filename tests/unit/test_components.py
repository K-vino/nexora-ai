import pytest
import pandas as pd
from nexora.validation.schema_validator import SchemaValidator
from nexora.feature_engineering.auto_imputer import AutoImputer

def test_validator_detects_empty_df():
    """Unit Test: Ensure validator catches empty dataframes."""
    df = pd.DataFrame()
    validator = SchemaValidator()
    assert validator.validate(df) == False
    assert "DataFrame is empty." in validator.get_validation_report()["errors"]

def test_imputer_fills_nans():
    """Unit Test: Ensure imputer fills NaN values correctly."""
    df = pd.DataFrame({"A": [1, 2, None], "B": ["x", None, "y"]})
    imputer = AutoImputer()
    df_clean = imputer.fit_transform(df)
    
    assert df_clean["A"].isnull().sum() == 0
    assert df_clean["B"].isnull().sum() == 0
    assert df_clean.iloc[2]["A"] == 1.5 # Median of 1, 2
    assert df_clean.iloc[1]["B"] == "x" # Mode of x, y (if tie, picks first) or y
