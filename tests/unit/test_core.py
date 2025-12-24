import pytest
import pandas as pd
from nexora.ingestion.csv_connector import CSVConnector
from nexora.validation.schema_validator import SchemaValidator
from nexora.core.exceptions import DataIngestionError, ValidationError

def test_csv_connector_file_not_found():
    connector = CSVConnector()
    with pytest.raises(DataIngestionError):
        connector.load_data("non_existent.csv")

def test_schema_validator_empty_df():
    validator = SchemaValidator()
    df = pd.DataFrame()
    with pytest.raises(ValidationError):
        validator.validate(df)

def test_schema_validator_missing_columns():
    validator = SchemaValidator(required_columns=["A", "B"])
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(ValidationError):
        validator.validate(df)
