"""
Demo Script for Argus Platform
Quick demonstration of the public health intelligence system
"""

import sys
import os

# Add src to path
sys.path.append('src')

from run_argus import main

if _name_ == "_main_":
    print("🚀 ARGUS PLATFORM DEMO")
    print("=" * 50)
    print("Running complete public health intelligence pipeline...")
    print("This demonstrates:")
    print("✅ Clinical data ingestion & anomaly detection")
    print("✅ Twitter surveillance monitoring") 
    print("✅ Multi-source data fusion")
    print("✅ Risk assessment and alert generation")
    print("=" * 50)
    
    main()
