import pandas as pd
import numpy as np
import os

def generate_housing_data(n_rows=2000):
    np.random.seed(42)
    
    data = {
        'longitude': np.random.uniform(-124.35, -114.31, n_rows),
        'latitude': np.random.uniform(32.54, 41.95, n_rows),
        'housing_median_age': np.random.randint(1, 52, n_rows),
        'total_rooms': np.random.randint(100, 10000, n_rows),
        'total_bedrooms': np.random.randint(20, 2000, n_rows),
        'population': np.random.randint(50, 5000, n_rows),
        'households': np.random.randint(20, 2000, n_rows),
        'median_income': np.random.uniform(0.5, 15.0, n_rows),
        'ocean_proximity': np.random.choice(['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'], n_rows),
        # Target: median_house_value (correlated with income)
    }
    
    df = pd.DataFrame(data)
    # Add some noise and correlation
    df['median_house_value'] = (
        df['median_income'] * 40000 + 
        df['total_rooms'] * 20 + 
        np.random.normal(0, 50000, n_rows)
    )
    # Clip to realistic range
    df['median_house_value'] = df['median_house_value'].clip(15000, 500000)
    
    output_path = os.path.join("data", "housing.csv")
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {n_rows} rows of synthetic housing data at {output_path}")

if __name__ == "__main__":
    generate_housing_data()
