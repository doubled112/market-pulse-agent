"""
Stage 2: Process Agent
Job: read raw price data and turn it into display-ready figures.
Does NOT fetch data itself, does NOT publish anywhere — pure transformation.
"""

import json
from datetime import datetime, timezone

INPUT_PATH = "data/raw_prices.json"
OUTPUT_PATH = "data/processed_prices.json"

DISPLAY_NAMES = {
    "sp500": "S&P 500",
    "asx200": "ASX 200",
}

def process():
    with open(INPUT_PATH, "r") as f:
        raw = json.load(f)

    processed = {}
    for key, entry in raw["data"].items():
        if "error" in entry:
            processed[key] = {"name": DISPLAY_NAMES.get(key, key), "error": entry["error"]}
            continue

        latest = entry["latest_close"]
        previous = entry["previous_close"]
        change = latest - previous
        pct_change = (change / previous) * 100 if previous else 0

        processed[key] = {
            "name": DISPLAY_NAMES.get(key, key),
            "latest_close": latest,
            "change": round(change, 2),
            "pct_change": round(pct_change, 2),
            "as_of": entry["latest_date"],
        }

    output = {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "fetched_at": raw["fetched_at"],
        "indices": processed,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    return output

if __name__ == "__main__":
    result = process()
    print("Process complete. Saved to data/processed_prices.json")
    print(json.dumps(result, indent=2))