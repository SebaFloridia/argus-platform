# Data Directory

This directory contains generated surveillance data from the Argus Platform.

## Files

- clinical_data.csv - Synthetic clinical surveillance data with syndromes and cases
- clinical_anomalies.csv - Detected statistical anomalies in clinical data  
- twitter_surveillance.csv - Simulated Twitter symptom mention data
- fused_surveillance_data.csv - Multi-source fused data with risk scores

## Data Schema

### Clinical Data
- date: Date of observation (YYYY-MM-DD)
- state: US state code (CA, TX, FL, etc.)
- syndrome: Disease syndrome (COVID, ILI, RESPIRATORY, GASTROINTESTINAL)
- cases_reported: Number of reported cases
- population_coverage: Population denominator for rate calculation
- incidence_rate: Cases per 100,000 population
- cases_7d_avg: 7-day moving average of cases

### Twitter Data
- date: Date of observation
- state: US state code  
- symptom_category: Type of symptom mentioned (fever, cough, respiratory, gastrointestinal)
- tweet_count: Number of symptom-related tweets

### Fused Data
- Combined data from all sources with composite risk scores
- risk_level: Low/Medium/High risk assessment
