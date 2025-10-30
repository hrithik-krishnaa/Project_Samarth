# backend/clean_crop.py
import os, pandas as pd, numpy as np

RAW = os.path.join("data", "clean", "crop_production_live.csv")
OUT = os.path.join("data", "clean", "crop_prod.parquet")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

if not os.path.exists(RAW):
    raise FileNotFoundError(f"Raw crop file not found at {RAW}. Run fetch_crop_data first.")

print("Loading raw crop CSV:", RAW)
df = pd.read_csv(RAW, low_memory=False)
print("Columns found (sample):", df.columns.tolist()[:60])

def find_col(df, keywords):
    for c in df.columns:
        lc = c.lower()
        for k in keywords:
            if k in lc:
                return c
    return None

# Detect columns (auto)
state_col = find_col(df, ["state", "state_name"])
district_col = find_col(df, ["district", "dist"])
year_col = find_col(df, ["year", "crop_year", "cropyear", "season"])
crop_col = find_col(df, ["crop", "commodity", "crop_name"])
prod_col = find_col(df, ["production", "prod", "production_tonnes", "quantity"])
area_col = find_col(df, ["area", "harvest"])

print("Detected mapping:", state_col, district_col, year_col, crop_col, prod_col, area_col)

if not (state_col and year_col and crop_col and prod_col):
    raise ValueError("Could not auto-detect essential columns. Open the CSV and tell me the header line and I'll adapt the script.")

# Build canonical DF
df2 = pd.DataFrame()
df2["state"] = df[state_col].astype(str).str.strip().str.upper()
df2["district"] = df[district_col].astype(str).str.strip().str.upper() if district_col else np.nan
df2["crop"] = df[crop_col].astype(str).str.strip().str.upper()
df2["YEAR"] = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
df2["production_tonnes"] = pd.to_numeric(df[prod_col].astype(str).str.replace(",",""), errors="coerce")
df2["area"] = pd.to_numeric(df[area_col].astype(str).str.replace(",",""), errors="coerce") if area_col else np.nan

# Keep source (if present) or set resource page
if "source_url" in df.columns:
    df2["source_url"] = df["source_url"]
else:
    df2["source_url"] = "https://data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"

# Drop malformed rows
df2 = df2.dropna(subset=["YEAR","production_tonnes"])
df2.to_parquet(OUT, index=False)
print("Saved cleaned crop data to:", OUT)
print(df2.head().to_string(index=False))
