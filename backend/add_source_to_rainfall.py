import os
import pandas as pd

p = "data/clean/imd_rainfall_cleaned.csv"

print("Checking if rainfall file exists...")

if os.path.exists(p):
    print("✅ File found:", p)
    df = pd.read_csv(p)
    print("Columns detected:", df.columns.tolist()[:20])
    
    if "source_url" not in df.columns:
        df["source_url"] = "https://data.gov.in/organization/india-meteorological-department"
        df.to_csv(p, index=False)
        print("✅ Added source_url column successfully.")
    else:
        print("ℹ️  source_url column already exists.")
else:
    print("❌ Rainfall file not found. Please check your file path.")
