# check_overlap.py
import pandas as pd
r = pd.read_csv("data/clean/imd_rainfall_cleaned.csv")
c = pd.read_parquet("data/clean/crop_prod.parquet")
r_states = sorted(list(set(r['STATE'].dropna())))
c_states = sorted(list(set(c['STATE'].dropna())))
print("Rain states sample (first 30):", r_states[:30])
print("Crop states sample (first 30):", c_states[:30])
r_years = sorted(list(set(r['YEAR'].dropna())))
c_years = sorted(list(set(c['YEAR'].dropna())))
print("Rain years min..max:", (r_years[0] if r_years else None, r_years[-1] if r_years else None))
print("Crop years min..max:", (c_years[0] if c_years else None, c_years[-1] if c_years else None))
print("Intersection years (sample up to 30):", sorted(list(set(r_years).intersection(set(c_years))))[:30])
