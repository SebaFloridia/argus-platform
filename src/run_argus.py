"""
Argus Platform - Public Health Intelligence System
Main pipeline runner
"""

import os
import sys
import pandas as pd

def run_clinical_module():
    print("🧬 Running Clinical Data Ingestion...")
    try:
        sys.path.append('data_ingestion')
        from clinical_data_ingestion import main
        clinical_data, anomalies = main()
        print("✅ Clinical data generated successfully")
        return True
    except Exception as e:
        print(f"❌ Clinical module failed: {e}")
        return False

def run_twitter_module():
    print("🐦 Running Twitter Surveillance...")
    try:
        from twitter_simple import main
        twitter_data = main()
        print("✅ Twitter data generated successfully")
        return True
    except Exception as e:
        print(f"❌ Twitter module failed: {e}")
        return False

def run_fusion_module():
    print("🔗 Running Data Fusion Engine...")
    try:
        from data_fusion_simple import main
        fused_data = main()
        print("✅ Data fusion completed successfully")
        return True
    except Exception as e:
        print(f"❌ Fusion module failed: {e}")
        return False

def main():
    print("🚀 ARGUS PLATFORM - Public Health Intelligence System")
    print("=" * 60)
    
    # Run all modules
    clinical_success = run_clinical_module()
    twitter_success = run_twitter_module() 
    fusion_success = run_fusion_module()
    
    print("\n" + "=" * 60)
    print("📊 PIPELINE SUMMARY")
    print(f"Clinical Data: {'✅ SUCCESS' if clinical_success else '❌ FAILED'}")
    print(f"Twitter Surveillance: {'✅ SUCCESS' if twitter_success else '❌ FAILED'}")
    print(f"Data Fusion: {'✅ SUCCESS' if fusion_success else '❌ FAILED'}")
    
    # Show generated files
    print("\n📁 GENERATED FILES:")
    data_files = [
        "data/clinical_data.csv",
        "data/clinical_anomalies.csv",
        "data/twitter_surveillance.csv", 
        "data/fused_surveillance_data.csv"
    ]
    
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} (missing)")
    
    if clinical_success and os.path.exists("data/clinical_anomalies.csv"):
        anomalies_df = pd.read_csv("data/clinical_anomalies.csv")
        print(f"\n🚨 ALERTS: {len(anomalies_df)} anomalies detected")
        if len(anomalies_df) > 0:
            print("Top anomalies in CA/TX (recent outbreaks):")
            recent_ca_tx = anomalies_df[
                (anomalies_df['state'].isin(['CA', 'TX'])) & 
                (anomalies_df['date'] > '2025-11-10')
            ].head(3)
            print(recent_ca_tx[['date', 'state', 'syndrome', 'anomaly_magnitude']].to_string(index=False))
    
    print("\n🎉 Argus Platform pipeline completed!")
    print("Next: Build interactive dashboard with Streamlit")

if __name__ == "__main__":
    main()
