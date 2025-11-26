"""
Twitter Surveillance Module for Argus Platform
Monitors social media for disease-related mentions and symptoms
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import List, Dict

class TwitterSurveillance:
    """
    Simulates Twitter data monitoring for syndromic surveillance
    """
    
    def _init_(self):
        self.symptom_keywords = {
            'fever': ['fever', 'hot', 'sweating', 'chills'],
            'cough': ['cough', 'coughing', 'hacking'],
            'respiratory': ['breathing', 'shortness of breath', 'wheezing'],
            'gastrointestinal': ['nausea', 'vomiting', 'diarrhea', 'stomach'],
            'fatigue': ['tired', 'fatigue', 'exhausted', 'weak']
        }
        self.states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    
    def simulate_twitter_data(self, days: int = 30) -> pd.DataFrame:
        """
        Simulates Twitter data with disease-related mentions
        """
        print(\"Generating synthetic Twitter surveillance data...\")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = [start_date + timedelta(days=x) for x in range(days)]
        
        data = []
        
        for date in dates:
            for state in self.states:
                # Base tweet volume with daily variation
                base_tweets = np.random.poisson(1000)  # Average 1000 tweets per state per day
                
                # Add outbreak signals
                outbreak_factor = 1.0
                if date > end_date - timedelta(days=7) and state in ['CA', 'TX']:
                    outbreak_factor = 3.0  # Simulate recent outbreak in CA and TX
                
                total_tweets = int(base_tweets * outbreak_factor)
                
                # Distribute tweets across symptoms
                for symptom_category, keywords in self.symptom_keywords.items():
                    # Different base rates per symptom
                    symptom_rates = {
                        'fever': 0.15, 'cough': 0.20, 'respiratory': 0.12,
                        'gastrointestinal': 0.10, 'fatigue': 0.08
                    }
                    
                    symptom_tweets = int(total_tweets * symptom_rates[symptom_category])
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'state': state,
                        'symptom_category': symptom_category,
                        'tweet_count': symptom_tweets,
                        'data_source': 'Simulated_Twitter_Surveillance'
                    })
        
        df = pd.DataFrame(data)
        print(f\"Generated {len(df)} records of Twitter surveillance data\")
        return df
    
    def detect_twitter_anomalies(self, df: pd.DataFrame, threshold_std: float = 2.5) -> pd.DataFrame:
        """
        Detects anomalous tweet volumes using statistical methods
        """
        anomalies = []
        
        for state in df['state'].unique():
            for symptom in df['symptom_category'].unique():
                subset = df[(df['state'] == state) & (df['symptom_category'] == symptom)].copy()
                
                if len(subset) > 7:
                    # Calculate z-scores for tweet counts
                    mean_tweets = subset['tweet_count'].mean()
                    std_tweets = subset['tweet_count'].std()
                    
                    if std_tweets > 0:  # Avoid division by zero
                        subset['z_score'] = (subset['tweet_count'] - mean_tweets) / std_tweets
                        
                        # Flag anomalies
                        anomalous_days = subset[subset['z_score'] > threshold_std]
                        
                        for _, row in anomalous_days.iterrows():
                            anomalies.append({
                                'date': row['date'],
                                'state': state,
                                'symptom_category': symptom,
                                'tweet_count': row['tweet_count'],
                                'z_score': round(row['z_score'], 2),
                                'expected_tweets': round(mean_tweets, 2),
                                'anomaly_magnitude': round(row['tweet_count'] - mean_tweets, 2)
                            })
        
        return pd.DataFrame(anomalies)

def main():
    """Test the Twitter surveillance module"""
    twitter_monitor = TwitterSurveillance()
    
    # Generate synthetic data
    twitter_df = twitter_monitor.simulate_twitter_data(days=60)
    
    # Detect anomalies
    twitter_anomalies = twitter_monitor.detect_twitter_anomalies(twitter_df)
    
    print(f\"\\n=== TWITTER SURVEILLANCE SUMMARY ===\")
    print(f\"Total records: {len(twitter_df)}\")
    print(f\"Date range: {twitter_df['date'].min()} to {twitter_df['date'].max()}\")
    print(f\"States monitored: {len(twitter_df['state'].unique())}\")
    print(f\"Symptom categories: {list(twitter_df['symptom_category'].unique())}\")
    print(f\"Twitter anomalies detected: {len(twitter_anomalies)}\")
    
    if len(twitter_anomalies) > 0:
        print(f\"\\n=== TOP 5 TWITTER ANOMALIES ===\")
        print(twitter_anomalies.head().to_string(index=False))
    
    # Save the data
    twitter_df.to_csv('../data/twitter_surveillance.csv', index=False)
    twitter_anomalies.to_csv('../data/twitter_anomalies.csv', index=False)
    
    print(f\"\\nData saved to:\")
    print(f\"- ../data/twitter_surveillance.csv\")
    print(f\"- ../data/twitter_anomalies.csv\")
    
    return twitter_df, twitter_anomalies

if _name_ == \"_main_\":
    twitter_data, twitter_anomalies = main()
