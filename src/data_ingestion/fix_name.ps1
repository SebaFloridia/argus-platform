# TEMPORARY FIX - Run this to fix the main file
content = Get-Content "clinical_data_ingestion.py"
 =  -replace 'if name == "main":', 'if _name_ == "_main_":'
 | Set-Content "clinical_data_ingestion.py"
Write-Host "File fixed! Now run: python clinical_data_ingestion.py"
