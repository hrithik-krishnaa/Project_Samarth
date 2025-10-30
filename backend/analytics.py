import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# -------------------------------
# 1️⃣ Compare rainfall across states
# -------------------------------
def compare_rain_and_crops():
    try:
        rain = pd.read_csv("data/clean/imd_rainfall_cleaned.csv")
        crop = pd.read_csv("data/clean/crop_production_cleaned.csv")

        # Ensure proper string formatting
        rain["state"] = rain["state"].astype(str).str.upper().str.strip()
        crop["STATE"] = crop["STATE"].astype(str).str.upper().str.strip()

        # Calculate average annual rainfall
        annual_rain = rain.groupby("state")["rain_mm"].mean().reset_index()
        annual_rain.rename(columns={"state": "STATE", "rain_mm": "avg_annual_rain_mm"}, inplace=True)

        return annual_rain.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# 2️⃣ District-level extremes
# -------------------------------
def district_extremes(state, crop_name):
    try:
        rain = pd.read_csv("data/clean/imd_rainfall_cleaned.csv")
        crop = pd.read_csv("data/clean/crop_production_cleaned.csv")

        # Ensure string columns are consistent
        rain["state"] = rain["state"].astype(str).str.upper().str.strip()
        crop["STATE"] = crop["STATE"].astype(str).str.upper().str.strip()
        crop["DISTRICT"] = crop["DISTRICT"].astype(str).str.upper().str.strip()
        crop["CROP"] = crop["CROP"].astype(str).str.upper().str.strip()

        state = state.upper().strip()
        crop_name = crop_name.upper().strip()

        subset = crop[(crop["STATE"] == state) & (crop["CROP"] == crop_name)]

        if subset.empty:
            return {"error": "No records for this crop and states"}

        grouped = subset.groupby("DISTRICT")["PRODUCTION_TONNES"].sum().reset_index()
        max_district = grouped.loc[grouped["PRODUCTION_TONNES"].idxmax()]
        min_district = grouped.loc[grouped["PRODUCTION_TONNES"].idxmin()]

        return {
            "max_district": max_district.to_dict(),
            "min_district": min_district.to_dict(),
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# 3️⃣ Rainfall vs Crop Trend Correlation
# -------------------------------
def trend_and_correlation(state, crop_name):
    try:
        rain = pd.read_csv("data/clean/imd_rainfall_cleaned.csv")
        crop = pd.read_csv("data/clean/crop_production_cleaned.csv")

        # Ensure proper string formatting
        rain["state"] = rain["state"].astype(str).str.upper().str.strip()
        crop["STATE"] = crop["STATE"].astype(str).str.upper().str.strip()
        crop["CROP"] = crop["CROP"].astype(str).str.upper().str.strip()

        state = state.upper().strip()
        crop_name = crop_name.upper().strip()

        rain_state = rain[rain["state"] == state]
        crop_state = crop[(crop["STATE"] == state) & (crop["CROP"] == crop_name)]

        if rain_state.empty or crop_state.empty:
            return {"error": "No matching state or crop data"}

        rain_yearly = rain_state.groupby("year")["rain_mm"].sum().reset_index()
        crop_yearly = crop_state.groupby("YEAR")["PRODUCTION_TONNES"].sum().reset_index()

        combined = pd.merge(rain_yearly, crop_yearly, left_on="year", right_on="YEAR", how="inner")
        combined.rename(columns={"rain_mm": "rain_mm", "PRODUCTION_TONNES": "production"}, inplace=True)

        if combined["production"].nunique() <= 1 or combined["rain_mm"].nunique() <= 1:
            r, p = None, None
        else:
            r, p = pearsonr(combined["production"], combined["rain_mm"])

        return {
            "years": combined["year"].tolist(),
            "combined": combined.to_dict(orient="records"),
            "pearson_r": r,
            "p_value": p,
            "sources": [
                "https://data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de",
                "https://data.gov.in/organization/india-meteorological-department",
            ],
        }

    except Exception as e:
        return {"error": str(e)}
