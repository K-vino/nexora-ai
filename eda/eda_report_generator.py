import pandas as pd
import numpy as np
from typing import Dict, Any, List
from utils.data_types import DataBundle
from utils.logging import Logger

class EdaReportGenerator:
    """
    Generates structured exploratory data analysis insights.
    """
    def __init__(self):
        self.logger = Logger.get_logger("EdaReportGenerator")

    def run(self, bundle: DataBundle) -> DataBundle:
        """
        Analyzes the data and attaches structured findings to the bundle.
        """
        df = bundle.data  # Analyze raw data or features? Usually raw for EDA insights, or both.
        # Let's analyze the raw data (cleaned version if available in bundle.data after cleaning)
        
        self.logger.info("Starting EDA...")
        insights: Dict[str, Any] = {
            "key_findings": [],
            "risks": [],
            "suggested_next_steps": [],
            "correlations": {}
        }
        
        # 1. Descriptive Stats Findings
        for col in df.select_dtypes(include=[np.number]).columns:
            mean_val = df[col].mean()
            std_dev = df[col].std()
            cv = std_dev / mean_val if mean_val != 0 else 0
            
            if cv > 1.0:
                insights["key_findings"].append(f"High variance detected in '{col}' (CV > 1.0).")
                insights["risks"].append(f"High variance in {col}")
                insights["suggested_next_steps"].append(f"Consider log transformation or robust scaling for '{col}'.")
                
        # 2. Correlations
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            corr_matrix = numeric_df.corr().abs()
            # Select upper triangle of correlation matrix
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            
            # Find index of feature columns with correlation greater than 0.8
            high_corr = [column for column in upper.columns if any(upper[column] > 0.8)]
            
            for col in high_corr:
                correlated_feats = upper.index[upper[col] > 0.8].tolist()
                for feat in correlated_feats:
                    insights["key_findings"].append(f"Strong correlation ({upper.loc[feat, col]:.2f}) between '{feat}' and '{col}'.")
                    insights["correlations"][f"{feat}_vs_{col}"] = float(upper.loc[feat, col])
            
            if high_corr:
                insights["risks"].append("Multicollinearity detected.")
                insights["suggested_next_steps"].append("Consider dropping redundant correlated features or using PCA.")

        # 3. Anomaly Flags (Reuse quality report info if available)
        if bundle.quality_report and "outliers" in bundle.quality_report:
            total_outliers = sum(bundle.quality_report["outliers"].values())
            if total_outliers > 0:
                insights["key_findings"].append(f"Detected {total_outliers} total outliers across features.")
                insights["risks"].append("Outliers present.")
        
        # 4. Target Analysis (Heuristic: Try to guess target or use last column)
        # For this generic phase, we just note distribution of the last column if numeric
        last_col = df.columns[-1]
        if pd.api.types.is_numeric_dtype(df[last_col]):
             insights["key_findings"].append(f"Potential target '{last_col}' has mean {df[last_col].mean():.2f}")

        bundle.eda_insights = insights
        bundle.metadata["reasoning"].append("Generated structured EDA insights.")
        self.logger.info("EDA complete.")
        
        return bundle
