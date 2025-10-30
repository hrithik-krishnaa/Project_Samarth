# normalize_datasets.py
import pandas as pd, os

# Paths
rain_path = os.path.join("data","clean","imd_rainfall_cleaned.csv")
crop_parquet = os.path.join("data","clean","crop_prod.parquet")
crop_csv = os.path.join("data","clean","crop_production_live.csv")
crop_csv2 = os.path.join("data","clean","crop_production_cleaned.csv")

# Load rainfall
r = pd.read_csv(rain_path)
# normalize rainfall state/year/annual column names --- detect flexible names
if "subdivision" in r.columns:
    r.rename(columns={"subdivision":"STATE"}, inplace=True)
elif "state" in r.columns:
    r.rename(columns={"state":"STATE"}, inplace=True)
if "year" in r.columns:
    r.rename(columns={"year":"YEAR"}, inplace=True)
# find annual column
for c in r.columns:
    if c.lower().strip()=="annual" or "annual" in c.lower():
        r.rename(columns={c:"RAIN_MM"}, inplace=True)
        break
# standardize values
r["STATE"] = r["STATE"].astype(str).str.upper().str.strip()
r["YEAR"] = pd.to_numeric(r["YEAR"], errors="coerce").astype("Int64")
r.to_csv(rain_path, index=False)
print("Rain normalized and saved:", rain_path)

# Load crop (parquet preferred)
if os.path.exists(crop_parquet):
    c = pd.read_parquet(crop_parquet)
    src = crop_parquet
elif os.path.exists(crop_csv):
    c = pd.read_csv(crop_csv, low_memory=False)
    src = crop_csv
elif os.path.exists(crop_csv2):
    c = pd.read_csv(crop_csv2, low_memory=False)
    src = crop_csv2
else:
    raise FileNotFoundError("No crop source found")

# Uppercase all column names for canonical detection
c.columns = [str(x).upper() for x in c.columns]

# Map common column names
if "STATE" not in c.columns and "STATE_NAME" in c.columns:
    c.rename(columns={"STATE_NAME":"STATE"}, inplace=True)
if "YEAR" not in c.columns:
    # try common variants
    for k in ["CROP_YEAR","YEAR_OF_DATA","SEASON_YEAR","YEAR_"]:
        if k in c.columns:
            c.rename(columns={k:"YEAR"}, inplace=True)
            break
# production column
if "PRODUCTION_TONNES" not in c.columns:
    for k in ["PRODUCTION","PROD","PRODUCTION_QTY","PRODUCTION_QUANTITY","PRODUCTION_TONNES"]:
        if k in c.columns:
            c.rename(columns={k:"PRODUCTION_TONNES"}, inplace=True)
            break

# crop column
if "CROP" not in c.columns:
    for k in ["COMMODITY","CROP_NAME","CROP_TYPE","CROP_DESC"]:
        if k in c.columns:
            c.rename(columns={k:"CROP"}, inplace=True)
            break

# normalize fields
if "STATE" in c.columns:
    c["STATE"] = c["STATE"].astype(str).str.upper().str.strip()
if "YEAR" in c.columns:
    c["YEAR"] = pd.to_numeric(c["YEAR"], errors="coerce").astype("Int64")
if "CROP" in c.columns:
    c["CROP"] = c["CROP"].astype(str).str.upper().str.strip()
if "PRODUCTION_TONNES" in c.columns:
    c["PRODUCTION_TONNES"] = pd.to_numeric(c["PRODUCTION_TONNES"].astype(str).str.replace(",","").str.replace(" ",""), errors="coerce")

# Save canonical parquet and csv
out_parquet = os.path.join("data","clean","crop_prod.parquet")
out_csv = os.path.join("data","clean","crop_production_cleaned.csv")
c.to_parquet(out_parquet, index=False)
c.to_csv(out_csv, index=False)
print("Crop normalized and saved to:", out_parquet, "and", out_csv)
print("Sample STATES:", list(c['STATE'].dropna().unique())[:20])
print("Sample YEARS (first 20):", sorted(list(c['YEAR'].dropna().unique())[:20]))
print("Sample CROP names (first 20):", list(c['CROP'].dropna().unique())[:20])
