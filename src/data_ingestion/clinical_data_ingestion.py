"""
Clinical Data Ingestion Module for Argus Platform
Fetches and processes syndromic surveillance data from public health APIs
"""

import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time
import os
from typing import Dict, List, Optional
import numpy as np

class ClinicalDataIngestor:
    """
    Ingests clinical syndromic surveillance data from public health data sources
    """
    
    def __init__(self):
        self.base_urls = {
            'cdc': 'https://data.cdc.gov/resource/',
            'who': 'https://ghoapi.azureedge.net/api/'
        }
        self.syndromes = ['ILI', 'COVID', 'RESPIRATORY', 'GASTROINTESTINAL']
        
    def simulate_clinical_data(self, days: int = 90) -> pd.DataFrame:
        """
        Simulates clinical syndromic surveillance data when real APIs are unavailable
        This creates realistic synthetic data for demonstration
        """
        print("Generating synthetic clinical surveillance data...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dates = [start_date + timedelta(days=x) for x in range(days)]
        states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        
        data = []
        
        for date in dates:
            for state in states:
                # Base rates with seasonal variation
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 0.5 * np.sin(2 * np.pi * day_of_year / 365)
                
                # Add some outbreak signals
                outbreak_factor = 1.0
                if date > end_date - timedelta(days=14) and state in ['CA', 'TX']:
                    outbreak_factor = 2.5  # Simulate recent outbreak
                
                for syndrome in self.syndromes:
                    # Different base rates per syndrome
                    syndrome_rates = {
                        'ILI': 0.015,
                        'COVID': 0.008,
                        'RESPIRATORY': 0.025,
                        'GASTROINTESTINAL': 0.012
                    }
                    
                    rate = syndrome_rates[syndrome] * (1 + seasonal_factor) * outbreak_factor
                    cases = max(0, int(np.random.poisson(rate * 1000000 / len(states))))
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'state': state,
                        'syndrome': syndrome,
                        'cases_reported': cases,
                        'population_coverage': 1000000 / len(states),
                        'data_source': 'Simulated_Syndromic_Surveillance'
                    })
        
        df = pd.DataFrame(data)
        print(f"Generated {len(df)} records of clinical surveillance data")
        return df
    
    def calculate_epidemiological_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates key epidemiological metrics from clinical data
        """
        # Calculate incidence rates per 100,000
        df['incidence_rate'] = (df['cases_reported'] / df['population_coverage']) * 100000
        
        # Calculate 7-day moving averages for trend analysis
        df = df.sort_values(['state', 'syndrome', 'date'])
        df['cases_7d_avg'] = df.groupby(['state', 'syndrome'])['cases_reported'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
        
        # Calculate percent change from previous period
        df['pct_change'] = df.groupby(['state', 'syndrome'])['cases_reported'].pct_change()
        
        return df
    
    def detect_anomalies(self, df: pd.DataFrame, threshold_std: float = 2.0) -> pd.DataFrame:
        """
        Detects anomalous case counts using statistical methods
        """
        anomalies = []
        
        for state in df['state'].unique():
            for syndrome in df['syndrome'].unique():
                subset = df[(df['state'] == state) & (df['syndrome'] == syndrome)].copy()
                
                if len(subset) > 7:
                    # Calculate z-scores
                    mean_cases = subset['cases_reported'].mean()
                    std_cases = subset['cases_reported'].std()
                    
                    subset['z_score'] = (subset['cases_reported'] - mean_cases) / std_cases
                    
                    # Flag anomalies
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
    """Test the clinical data ingestion"""
    ingestor = ClinicalDataIngestor()
    
    # Generate synthetic data
    clinical_df = ingestor.simulate_clinical_data(days=120)
    
    # Calculate metrics
    clinical_df = ingestor.calculate_epidemiological_metrics(clinical_df)
    
    # Detect anomalies
    anomalies = ingestor.detect_anomalies(clinical_df)
    
    print(f"\n=== CLINICAL DATA SUMMARY ===")
    print(f"Total records: {len(clinical_df)}")
    print(f"Date range: {clinical_df['date'].min()} to {clinical_df['date'].max()}")
    print(f"States covered: {len(clinical_df['state'].unique())}")
    print(f"Syndromes monitored: {list(clinical_df['syndrome'].unique())}")
    print(f"Anomalies detected: {len(anomalies)}")
    
    if len(anomalies) > 0:
        print(f"\n=== TOP 5 ANOMALIES DETECTED ===")
        print(anomalies.head().to_string(index=False))
    
    # Save the data
    clinical_df.to_csv('../data/clinical_data.csv', index=False)
    anomalies.to_csv('../data/clinical_anomalies.csv', index=False)
    
    print(f"\nData saved to:")
    print(f"- ../data/clinical_data.csv")
    print(f"- ../data/clinical_anomalies.csv")
    
    return clinical_df, anomalies

# CORRECTED - Using double underscores: _name_ and _main_
if __name__ == "__main__":
    clinical_data, anomalies = main()
