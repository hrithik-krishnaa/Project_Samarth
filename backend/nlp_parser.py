# nlp_parser.py
import re
import pandas as pd

# load canonical lists once
RAIN_FILE = "data/clean/imd_rainfall_cleaned.csv"
CROP_FILE = "data/clean/crop_production_cleaned.csv"

def _load_state_list():
    try:
        r = pd.read_csv(RAIN_FILE, low_memory=False)
        if "state" in r.columns:
            states = sorted(r["state"].astype(str).str.upper().str.strip().unique().tolist())
            return states
    except Exception:
        pass
    # fallback minimal list
    return []

def _load_crop_list():
    try:
        c = pd.read_csv(CROP_FILE, low_memory=False)
        if "CROP" in c.columns:
            crops = sorted(c["CROP"].astype(str).str.upper().str.strip().unique().tolist())
            return crops
    except Exception:
        pass
    return []

STATES = _load_state_list()
CROPS = _load_crop_list()

def find_state_tokens(text):
    text_u = text.upper()
    hits = []
    for s in STATES:
        if s and s in text_u:
            hits.append(s)
    return sorted(list(dict.fromkeys(hits)))  # unique preserve order

def find_crop_tokens(text):
    text_u = text.upper()
    hits = []
    for crop in CROPS:
        if crop and crop in text_u:
            hits.append(crop)
    return sorted(list(dict.fromkeys(hits)))

def extract_integers(text):
    # returns all integers mentioned
    nums = [int(n) for n in re.findall(r"\b([0-9]{1,4})\b", text)]
    return nums

def parse_question(text):
    """
    Returns: dict with
      - type: 'compare' | 'district' | 'trend' | 'unknown'
      - states: list of matched states (uppercase)
      - crop: first matched crop or None
      - n_years: number (int) or default 5
      - top_m: number (int) or default 3
    """
    out = {"type": "unknown", "states": [], "crop": None, "n_years": 5, "top_m": 3, "raw": text}

    t = text.strip()
    # detect intent by keywords
    t_low = t.lower()
    if any(k in t_low for k in ["compare", "vs", "difference", "average"]):
        out["type"] = "compare"
    if any(k in t_low for k in ["district", "highest", "lowest", "top district", "which district"]):
        out["type"] = "district"
    if any(k in t_low for k in ["trend", "correlate", "correlation", "correlate", "impact", "analysis"]):
        out["type"] = "trend"
    # fallback: prefer compare
    if out["type"] == "unknown":
        out["type"] = "compare"

    # extract states and crops
    out["states"] = find_state_tokens(t)
    crops = find_crop_tokens(t)
    out["crop"] = crops[0] if crops else None

    # extract numeric hints
    nums = extract_integers(t)
    # heuristics: if "last N" or "past N" present, use first small int as n_years
    m_last = re.search(r"(last|past|previous)\s+([0-9]{1,4})\s+year", t_low)
    if m_last:
        out["n_years"] = int(m_last.group(2))
    else:
        # if any int and < 30, use as either years or top_m depending on words
        if nums:
            # check for "top M"
            m_top = re.search(r"top\s+([0-9]{1,3})", t_low)
            if m_top:
                out["top_m"] = int(m_top.group(1))
            elif any(w in t_low for w in ["last", "past", "previous"]):
                out["n_years"] = nums[0]
            else:
                # ambiguous: treat first as n_years if >5 else top_m
                first = nums[0]
                if first > 5:
                    out["n_years"] = first
                else:
                    out["top_m"] = first

    # defaults if no states: keep empty; caller may decide defaults
    return out
