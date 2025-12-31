import pandas as pd
import numpy as np
from utils.data_types import DataBundle
from utils.logging import Logger
from sklearn.preprocessing import StandardScaler, LabelEncoder # type: ignore

class DataCleaner:
    def __init__(self):
        self.logger = Logger.get_logger("DataCleaner")
        
    def clean(self, bundle: DataBundle) -> DataBundle:
        df = bundle.data.copy()
        reasoning = []
        
        # Simple imputation: Fill numeric missing with Median, object with Mode
        for col in df.columns:
            if df[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)
                    reasoning.append(f"Imputed missing values in '{col}' with median: {median_val}")
                else:
                    mode_val = df[col].mode()[0]
                    df[col] = df[col].fillna(mode_val)
                    reasoning.append(f"Imputed missing values in '{col}' with mode: {mode_val}")
        
        bundle.data = df
        bundle.metadata["reasoning"].extend(reasoning)
        self.logger.info("Data cleaning (imputation) complete.")
        return bundle

class FeatureBuilder:
    def __init__(self):
        self.logger = Logger.get_logger("FeatureBuilder")
        self.cleaner = DataCleaner()
        
    def run(self, bundle: DataBundle) -> DataBundle:
        # First clean the data
        bundle = self.cleaner.clean(bundle)
        df = bundle.data
        features = df.copy()
        reasoning = []
        
        # Encoding Categoricals
        label_encoders = {}
        for col in features.select_dtypes(include=['object', 'category']).columns:
            le = LabelEncoder()
            features[col] = le.fit_transform(features[col].astype(str))
            label_encoders[col] = le
            reasoning.append(f"Label Encoded categorical column: '{col}'")
            
        # Scaling Numerics (if high variance/magnitude difference detection? For Phase 1 we apply Standard Scaler)
        # Filter target if known? For Phase 1 we treat all as potential features or just scale numerics.
        # Assuming 'housing.csv', usually 'median_house_value' is target. We'll verify columns in main if needed.
        # For now, scale all numerics for demonstration of logic.
        
        scaler = StandardScaler()
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            features[numeric_cols] = scaler.fit_transform(features[numeric_cols])
            reasoning.append("Applied StandardScaler to all numerical features to normalize distribution.")
            
        bundle.features = features
        bundle.metadata["reasoning"].extend(reasoning)
        self.logger.info("Feature engineering complete.")
        return bundle
