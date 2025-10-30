import requests
import pandas as pd
import os

# 1️⃣ API details
API_URL = "https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"
API_KEY = "579b464db66ec23bdd00000163d43ca13f414fd75a942420a8f97918"

# 2️⃣ Parameters
params = {
    "api-key": API_KEY,
    "format": "json",
    "limit": 1000  # fetch 1000 rows at once
}

print("🔍 Step 1: Sending request to data.gov.in API...")

try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    print("✅ Step 2: Successfully fetched data from the API!")
except requests.exceptions.RequestException as e:
    print("❌ API Request failed:", e)
    exit()

# 3️⃣ Convert JSON to DataFrame
data = response.json()

if "records" in data:
    print(f"📊 Step 3: Found {len(data['records'])} records. Converting to DataFrame...")
    df = pd.DataFrame(data["records"])

    # 4️⃣ Save dataset
    os.makedirs("datasets", exist_ok=True)
    csv_path = os.path.join("datasets", "crop_data.csv")
    df.to_csv(csv_path, index=False)

    print(f"💾 Step 4: Data saved successfully at: {csv_path}")
    print("✅ Process complete! You can now open the CSV file to view the data.")
else:
    print("⚠️ No records found in API response.")
