"""
Clinical Data Ingestion Module for Argus Platform
Fetches and processes syndromic surveillance data from public health APIs
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ClinicalDataIngestor:
    def __init__(self):
        self.base_urls = {
            'cdc': 'https://data.cdc.gov/resource/',
            'who': 'https://ghoapi.azureedge.net/api/'
        }
        self.syndromes = ['ILI', 'COVID', 'RESPIRATORY', 'GASTROINTESTINAL']
        
    def simulate_clinical_data(self, days=90):
        print("Generating synthetic clinical surveillance data...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = [start_date + timedelta(days=x) for x in range(days)]
        states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        
        data = []
        for date in dates:
            for state in states:
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 0.5 * np.sin(2 * np.pi * day_of_year / 365)
                
                outbreak_factor = 1.0
                if date > end_date - timedelta(days=14) and state in ['CA', 'TX']:
                    outbreak_factor = 2.5
                
                for syndrome in self.syndromes:
                    syndrome_rates = {
                        'ILI': 0.015, 'COVID': 0.008, 
                        'RESPIRATORY': 0.025, 'GASTROINTESTINAL': 0.012
                    }
                    
                    rate = syndrome_rates[syndrome] * (1 + seasonal_factor) * outbreak_factor
                    cases = max(0, int(np.random.poisson(rate * 1000000 / len(states))))
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'state': state,
                        'syndrome': syndrome,
                        'cases_reported': cases,
                        'population_coverage': 1000000 / len(states),
                        'data_source': 'Clinical'
                    })
        
        df = pd.DataFrame(data)
        print(f"Generated {len(df)} clinical records")
        return df
    
    def calculate_epidemiological_metrics(self, df):
        df['incidence_rate'] = (df['cases_reported'] / df['population_coverage']) * 100000
        df = df.sort_values(['state', 'syndrome', 'date'])
        df['cases_7d_avg'] = df.groupby(['state', 'syndrome'])['cases_reported'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
        df['pct_change'] = df.groupby(['state', 'syndrome'])['cases_reported'].pct_change()
        return df
    
    def detect_anomalies(self, df, threshold_std=2.0):
        anomalies = []
        for state in df['state'].unique():
            for syndrome in df['syndrome'].unique():
                subset = df[(df['state'] == state) & (df['syndrome'] == syndrome)].copy()
                if len(subset) > 7:
                    mean_cases = subset['cases_reported'].mean()
                    std_cases = subset['cases_reported'].std()
                    subset['z_score'] = (subset['cases_reported'] - mean_cases) / std_cases
                    anomalous_days = subset[subset['z_score'] > threshold_std]
                    for _, row in anomalous_days.iterrows():
                        anomalies.append({
                            'date': row['date'],
                            'state': state,
                            'syndrome': syndrome,
                            'cases_reported': row['cases_reported'],
                            'z_score': round(row['z_score'], 2),
                            'expected_cases': round(mean_cases, 2),
                            'anomaly_magnitude': round(row['cases_reported'] - mean_cases, 2)
                        })
        return pd.DataFrame(anomalies)

def main():
    ingestor = ClinicalDataIngestor()
    clinical_df = ingestor.simulate_clinical_data(days=120)
    clinical_df = ingestor.calculate_epidemiological_metrics(clinical_df)
    anomalies = ingestor.detect_anomalies(clinical_df)
    
    print(f"Total records: {len(clinical_df)}")
    print(f"Date range: {clinical_df['date'].min()} to {clinical_df['date'].max()}")
    print(f"States: {len(clinical_df['state'].unique())}")
    print(f"Syndromes: {list(clinical_df['syndrome'].unique())}")
    print(f"Anomalies: {len(anomalies)}")
    
    clinical_df.to_csv('data/clinical_data.csv', index=False)
    anomalies.to_csv('data/clinical_anomalies.csv', index=False)
    print("Data saved to data/ folder")
    
    return clinical_df, anomalies

if __name__ == "__main__":
    clinical_data, anomalies = main()