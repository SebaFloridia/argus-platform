"""
Data Fusion Engine for Argus Platform
Integrates multiple data sources
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataFusionEngine:
    def _init_(self):
        self.data_sources = ['clinical', 'twitter', 'environmental']
    
    def load_and_fuse_data(self):
        print("Loading and fusing surveillance data...")
        
        try:
            # Load clinical data
            clinical_df = pd.read_csv('../data/clinical_data.csv')
            clinical_df['source'] = 'clinical'
            
            # Load Twitter data
            twitter_df = pd.read_csv('../data/twitter_surveillance.csv')
            twitter_df['source'] = 'twitter'
            
            # Create environmental data
            environmental_df = self.simulate_environmental_data()
            environmental_df['source'] = 'environmental'
            
            # Combine all data
            fused_data = pd.concat([clinical_df, twitter_df, environmental_df], ignore_index=True)
            
            print(f"Fused data from {len(fused_data['source'].unique())} sources")
            print(f"Total records: {len(fused_data)}")
            
            return fused_data
            
        except FileNotFoundError as e:
            print(f"Warning: {e}")
            return self.simulate_comprehensive_data()
    
    def simulate_environmental_data(self):
        dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
        states = ['CA', 'TX', 'FL', 'NY', 'IL']
        
        data = []
        for date in dates:
            for state in states:
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'state': state,
                    'temperature': round(np.random.normal(70, 15), 1),
                    'humidity': round(np.random.uniform(30, 90), 1),
                    'air_quality': round(np.random.uniform(0, 100), 1),
                    'data_source': 'Environmental'
                })
        
        return pd.DataFrame(data)
    
    def calculate_risk_scores(self, fused_df):
        df = fused_df.copy()
        
        # Simple risk calculation
        if 'cases_reported' in df.columns:
            max_cases = df['cases_reported'].max()
            if max_cases > 0:
                df['cases_risk'] = df['cases_reported'] / max_cases
        
        if 'tweet_count' in df.columns:
            max_tweets = df['tweet_count'].max()
            if max_tweets > 0:
                df['twitter_risk'] = df['tweet_count'] / max_tweets
        
        # Combine risks
        risk_components = []
        if 'cases_risk' in df.columns:
            risk_components.append(df['cases_risk'] * 0.6)
        if 'twitter_risk' in df.columns:
            risk_components.append(df['twitter_risk'] * 0.4)
        
        if risk_components:
            df['composite_risk'] = sum(risk_components)
            df['risk_level'] = pd.cut(df['composite_risk'], 
                                    bins=[0, 0.3, 0.7, 1.0], 
                                    labels=['Low', 'Medium', 'High'])
        
        return df

def main():
    fusion_engine = DataFusionEngine()
    fused_data = fusion_engine.load_and_fuse_data()
    risk_data = fusion_engine.calculate_risk_scores(fused_data)
    
    print(f"Data sources: {list(risk_data['source'].unique())}")
    
    if 'risk_level' in risk_data.columns:
        high_risk = len(risk_data[risk_data['risk_level'] == 'High'])
        print(f"High risk alerts: {high_risk}")
    
    risk_data.to_csv('../data/fused_surveillance_data.csv', index=False)
    print("Fused data saved to ../data/fused_surveillance_data.csv")
    
    return risk_data

if _name_ == "_main_":
    fused_data = main()
