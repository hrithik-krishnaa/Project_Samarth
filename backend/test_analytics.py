from analytics import compare_rain_and_crops, district_extremes, trend_and_correlation

# --- Test 1: Compare rainfall and crops ---
print("\n>>\nCOMPARE sample:")
try:
    result = compare_rain_and_crops()
    print(result[:2])  # show first 2 for clarity
except Exception as e:
    print("Error in compare_rain_and_crops:", e)

# --- Test 2: District extremes for a crop in a state ---
print("\nDISTRICTS sample:")
try:
    result = district_extremes("ANDHRA PRADESH", "RICE")
    print(result if result else "No data found")
except Exception as e:
    print("Error in district_extremes:", e)

# --- Test 3: Trend and correlation for a crop in a state ---
print("\nTREND sample (pearson r):")
try:
    result = trend_and_correlation("ANDHRA PRADESH", "RICE")
    print(result if result else "No data found")
except Exception as e:
    print("Error in trend_and_correlation:", e)
