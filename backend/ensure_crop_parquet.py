# backend/ensure_crop_parquet.py
import os, pandas as pd, numpy as np
from pathlib import Path

CLEAN_DIR = Path("data") / "clean"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# prefer existing parquet
PARQUET = CLEAN_DIR / "crop_prod.parquet"
CSV1 = CLEAN_DIR / "crop_production_cleaned.csv"
CSV2 = CLEAN_DIR / "crop_production_live.csv"   # fallback name
CSV3 = Path("datasets") / "crop_data.csv"       # possible earlier save

# Step A: find input
if PARQUET.exists():
    print("✅ Parquet already exists:", PARQUET)
    df = pd.read_parquet(PARQUET)
else:
    # choose best available CSV
    src = None
    for c in [CSV1, CSV2, CSV3]:
        if c.exists():
            src = c
            break
    if src is None:
        raise FileNotFoundError("No crop CSV or parquet found. Expected one of: {}, {}, {}, or crop_prod.parquet".format(CSV1, CSV2, CSV3))
    print("⤴️ Loading CSV:", src)
    df = pd.read_csv(src, low_memory=False)

# Show columns
print("Columns detected:", list(df.columns)[:60])

# Helper to detect column names
def find_col(df, keywords):
    for c in df.columns:
        lc = c.lower()
        for k in keywords:
            if k in lc:
                return c
    return None

state_c = find_col(df, ["state", "state_name"])
district_c = find_col(df, ["district", "dist"])
year_c = find_col(df, ["year", "crop_year", "cropyear"])
crop_c = find_col(df, ["crop", "commodity", "crop_name"])
prod_c = find_col(df, ["production", "prod", "production_tonnes", "production_qty", "production_quantity"])
area_c = find_col(df, ["area", "harvest"])

print("Auto-detected cols:", state_c, district_c, year_c, crop_c, prod_c, area_c)

if not (state_c and year_c and crop_c and prod_c):
    print("ERROR: could not detect essential columns automatically.")
    print("Please paste the header row (first line) of the CSV here so I can update detection.")
    raise SystemExit(1)

# Build canonical DF
dfc = pd.DataFrame()
dfc["state"] = df[state_c].astype(str).str.strip().str.upper()
dfc["district"] = df[district_c].astype(str).str.strip().str.upper() if district_c else np.nan
dfc["crop"] = df[crop_c].astype(str).str.strip().str.upper()
dfc["YEAR"] = pd.to_numeric(df[year_c], errors="coerce").astype("Int64")
dfc["production_tonnes"] = pd.to_numeric(df[prod_c].astype(str).str.replace(",","").str.replace(" ",""), errors="coerce")
dfc["area"] = pd.to_numeric(df[area_c].astype(str).str.replace(",",""), errors="coerce") if area_c else np.nan

if "source_url" in df.columns:
    dfc["source_url"] = df["source_url"]
else:
    dfc["source_url"] = f"https://data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"

# drop rows missing YEAR or production
dfc = dfc.dropna(subset=["YEAR","production_tonnes"])
PARQUET.parent.mkdir(parents=True, exist_ok=True)
dfc.to_parquet(PARQUET, index=False)
print("✅ Saved canonical parquet:", PARQUET)
print(dfc.head().to_string(index=False))
