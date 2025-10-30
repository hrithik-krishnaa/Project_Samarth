from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import difflib

app = FastAPI()

# Enable CORS so Streamlit frontend can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # Correct file paths
    rainfall_path = "data/clean/imd_rainfall_cleaned.csv"
    crop_path = "data/crop_production.csv"

    # Read data
    rainfall_df = pd.read_csv(rainfall_path)
    crop_df = pd.read_csv(crop_path)

    # Normalize state names and remove extra spaces
    rainfall_df["state"] = rainfall_df["state"].astype(str).str.strip().str.lower()
    crop_df["state_name"] = crop_df["state_name"].astype(str).str.strip().str.lower()

    # Add sample source URLs if missing
    if "source_url" not in rainfall_df.columns:
        rainfall_df["source_url"] = "https://data.gov.in/dataset/imd-rainfall"
    crop_df["source_url"] = "https://data.gov.in/dataset/agriculture-crop-production"

    print("✅ Data loaded successfully!")
    print("Available rainfall states:", sorted(rainfall_df["state"].unique()))
    print("Available crop states:", sorted(crop_df["state_name"].unique()))

except Exception as e:
    print("❌ Error loading data:", e)


@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}


def normalize(text):
    """Normalize names for comparison."""
    return str(text).strip().lower().replace("&", "and")


def find_closest_state(query_state, available_states):
    """Fuzzy match the state name (case-insensitive)."""
    query_state = normalize(query_state)
    matches = difflib.get_close_matches(query_state, available_states, n=1, cutoff=0.3)
    return matches[0] if matches else None


@app.post("/query")
def query_model(data: dict):
    question = data.get("question", "").lower().strip()

    if "compare" in question and "rainfall" in question:
        # Extract possible states from question
        states = []
        for s in rainfall_df["state"].unique():
            if s in question:
                states.append(s)

        # Try fuzzy match if exact match fails
        if len(states) < 2:
            for word in question.split():
                guess = find_closest_state(word, rainfall_df["state"].unique())
                if guess and guess not in states:
                    states.append(guess)

        if len(states) >= 2:
            s1, s2 = states[:2]

            # Calculate rainfall averages
            avg1 = round(rainfall_df[rainfall_df["state"] == s1]["rain_mm"].mean(), 2)
            avg2 = round(rainfall_df[rainfall_df["state"] == s2]["rain_mm"].mean(), 2)

            # Match crop data
            s1_match = find_closest_state(s1, crop_df["state_name"].unique())
            s2_match = find_closest_state(s2, crop_df["state_name"].unique())

            crops1 = (
                crop_df[crop_df["state_name"] == s1_match]["crop"]
                .value_counts()
                .head(3)
                .index.tolist()
                if s1_match
                else []
            )

            crops2 = (
                crop_df[crop_df["state_name"] == s2_match]["crop"]
                .value_counts()
                .head(3)
                .index.tolist()
                if s2_match
                else []
            )

            src1 = (
                rainfall_df[rainfall_df["state"] == s1]["source_url"].iloc[0]
                if "source_url" in rainfall_df.columns
                else "N/A"
            )
            src2 = (
                rainfall_df[rainfall_df["state"] == s2]["source_url"].iloc[0]
                if "source_url" in rainfall_df.columns
                else "N/A"
            )

            answer = (
                f"Average annual rainfall in {s1.title()} is about {avg1} mm, "
                f"while {s2.title()} receives around {avg2} mm. "
                f"Top crops grown are {', '.join(crops1) if crops1 else 'N/A'} in {s1.title()} "
                f"and {', '.join(crops2) if crops2 else 'N/A'} in {s2.title()}."
            )

            table = [
                {
                    "State": s1.title(),
                    "Avg Rainfall (mm)": avg1,
                    "Top Crops": ", ".join(crops1) if crops1 else "N/A",
                    "Source": src1,
                },
                {
                    "State": s2.title(),
                    "Avg Rainfall (mm)": avg2,
                    "Top Crops": ", ".join(crops2) if crops2 else "N/A",
                    "Source": src2,
                },
            ]

            return {"answer": answer, "table": table}

        return {"answer": "Please mention two valid states for comparison."}

    return {"answer": "Please ask a valid question about rainfall or crops."}
