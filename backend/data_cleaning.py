import pandas as pd
import os

RAW_DATA_PATH = os.path.join("data", "raw", "imd_rainfall.csv")
CLEAN_DATA_PATH = os.path.join("data", "clean", "imd_rainfall_cleaned.csv")

print("🔹 Reading dataset...")
try:
    df = pd.read_excel(RAW_DATA_PATH)
except:
    df = pd.read_csv(RAW_DATA_PATH)

print("✅ Dataset loaded successfully!")
print(df.head())

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("🧹 Cleaning data...")
df = df.dropna(how="all")
df = df.fillna(0)

os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
df.to_csv(CLEAN_DATA_PATH, index=False)
print(f"✅ Cleaned data saved to {CLEAN_DATA_PATH}")
