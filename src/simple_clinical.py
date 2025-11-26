import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=== ARGUS PLATFORM - CLINICAL DATA MODULE ===")

# Simple data generation
dates = [datetime.now() - timedelta(days=x) for x in range(30)]
states = ['CA', 'TX', 'NY']

data = []
for date in dates:
    for state in states:
        cases = np.random.poisson(50)  # Random cases around 50
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'state': state,
            'cases_reported': cases
        })

df = pd.DataFrame(data)
print(f"Generated {len(df)} records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total cases: {df['cases_reported'].sum()}")

# Save data
df.to_csv('../data/clinical_data_simple.csv', index=False)
print("Data saved to ../data/clinical_data_simple.csv")

print("SUCCESS: Clinical data module working!")
