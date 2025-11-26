"""
Twitter Surveillance Module for Argus Platform
Monitors social media for disease-related mentions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TwitterSurveillance:
    def _init_(self):
        self.symptom_keywords = {
            'fever': ['fever', 'hot', 'sweating'],
            'cough': ['cough', 'coughing'],
            'respiratory': ['breathing', 'shortness of breath'],
            'gastrointestinal': ['nausea', 'vomiting', 'diarrhea']
        }
        self.states = ['CA', 'TX', 'FL', 'NY', 'IL']
    
    def simulate_twitter_data(self, days=30):
        print("Generating synthetic Twitter surveillance data...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = [start_date + timedelta(days=x) for x in range(days)]
        
        data = []
        for date in dates:
            for state in self.states:
                base_tweets = np.random.poisson(1000)
                outbreak_factor = 1.0
                
                if date > end_date - timedelta(days=7) and state in ['CA', 'TX']:
                    outbreak_factor = 3.0
                
                total_tweets = int(base_tweets * outbreak_factor)
                
                for symptom_category in self.symptom_keywords.keys():
                    symptom_rates = {'fever': 0.15, 'cough': 0.20, 'respiratory': 0.12, 'gastrointestinal': 0.10}
                    symptom_tweets = int(total_tweets * symptom_rates[symptom_category])
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'state': state,
                        'symptom_category': symptom_category,
                        'tweet_count': symptom_tweets,
                        'data_source': 'Twitter'
                    })
        
        df = pd.DataFrame(data)
        print(f"Generated {len(df)} Twitter records")
        return df

def main():
    twitter_monitor = TwitterSurveillance()
    twitter_df = twitter_monitor.simulate_twitter_data(days=60)
    
    print(f"Twitter records: {len(twitter_df)}")
    print(f"Date range: {twitter_df['date'].min()} to {twitter_df['date'].max()}")
    
    twitter_df.to_csv('../data/twitter_surveillance.csv', index=False)
    print("Data saved to ../data/twitter_surveillance.csv")
    
    return twitter_df

if _name_ == "_main_":
    twitter_data = main()
