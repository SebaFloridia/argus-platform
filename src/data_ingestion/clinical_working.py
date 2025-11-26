import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def main():
    print("=== ARGUS PLATFORM - CLINICAL DATA INGESTION ===")
    print("Generating synthetic clinical surveillance data...")
    
    # Generate sample data
    dates = [datetime.now() - timedelta(days=x) for x in range(90)]
    states = ['CA', 'TX', 'FL', 'NY', 'IL']
    syndromes = ['ILI', 'COVID', 'RESPIRATORY']
    
    data = []
    for date in dates:
        for state in states:
            for syndrome in syndromes:
                cases = max(0, int(np.random.poisson(25)))
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'state': state,
                    'syndrome': syndrome,
                    'cases_reported': cases
                })
    
    df = pd.DataFrame(data)
    
    print(f"✓ Generated {len(df)} records")
    print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"✓ States: {len(df['state'].unique())}")
    print(f"✓ Syndromes: {len(df['syndrome'].unique())}")
    
    # Save data
    df.to_csv('../data/clinical_data.csv', index=False)
    print("✓ Data saved to ../data/clinical_data.csv")
    
    return df

# This line MUST be exactly like this:
if _name_ == "_main_":
    main()
