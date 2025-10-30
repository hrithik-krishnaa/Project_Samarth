# inspect_data_windows.py
import pandas as pd, os, json

print("PWD:", os.getcwd())

rain_path = os.path.join("data","clean","imd_rainfall_cleaned.csv")
crop_parquet = os.path.join("data","clean","crop_prod.parquet")
crop_csv = os.path.join("data","clean","crop_production_live.csv")
crop_csv2 = os.path.join("data","clean","crop_production_cleaned.csv")

print("\n--- Rainfall file check ---")
if not os.path.exists(rain_path):
    print("Rainfall file NOT found:", rain_path)
else:
    r = pd.read_csv(rain_path)
    print("rain shape:", r.shape)
    print("rain columns:", r.columns.tolist())
    print("rain sample (first 5):")
    print(r.head(5).to_string(index=False))

print("\n--- Crop file check (parquet preferred) ---")
crop_src = None
if os.path.exists(crop_parquet):
    crop_src = crop_parquet
elif os.path.exists(crop_csv):
    crop_src = crop_csv
elif os.path.exists(crop_csv2):
    crop_src = crop_csv2

if not crop_src:
    print("No crop file found at expected locations.")
else:
    print("Using crop source:", crop_src)
    if crop_src.endswith(".parquet"):
        c = pd.read_parquet(crop_src)
    else:
        c = pd.read_csv(crop_src, low_memory=False)
    print("crop shape:", c.shape)
    print("crop columns:", c.columns.tolist()[:80])
    print("crop sample (first 5):")
    print(c.head(5).to_string(index=False))
    # print some uniques for quick inspection
    cols_upper = [col.upper() for col in c.columns]
    c.columns = cols_upper
    if "STATE" in cols_upper:
        print("\nSample STATES (up to 30):", list(c["STATE"].dropna().unique())[:30])
    elif "STATE_NAME" in cols_upper:
        print("\nSample STATE_NAME (up to 30):", list(c["STATE_NAME"].dropna().unique())[:30])
    if "YEAR" in cols_upper:
        print("Sample YEARS (sorted first 20):", sorted(c["YEAR"].dropna().unique())[:20])
    if "CROP" in cols_upper:
        print("Sample CROP names (up to 30):", list(c["CROP"].dropna().unique())[:30])
