import pandas as pd

crop = pd.read_csv("data/clean/crop_production_cleaned.csv")

# Check if CROP column is numeric (which means it's actually the YEAR)
if pd.api.types.is_numeric_dtype(crop["CROP"]):
    print("⚠️ Detected that 'CROP' and 'YEAR' are swapped. Fixing...")

    # Swap the values (not just rename)
    crop["TEMP"] = crop["CROP"]
    crop["CROP"] = crop["YEAR"]
    crop["YEAR"] = crop["TEMP"]
    crop.drop(columns=["TEMP"], inplace=True)

    # Save the corrected version
    crop.to_csv("data/clean/crop_production_cleaned_fixed.csv", index=False)
    print("✅ Fixed version saved as crop_production_cleaned_fixed.csv")

else:
    print("✅ Columns are already correct.")

print("\n✅ Preview of fixed data:")
print(crop.head())

print("\nUnique CROP values:", crop["CROP"].unique()[:20])
