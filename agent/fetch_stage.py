"""
Stage 1: Fetch Agent
Job: retrieve raw index prices and save them as structured JSON.
Does NOT calculate anything or format for display — just gets the data.
"""

import yfinance as yf
import json
from datetime import datetime, timezone

TICKERS = {
    "sp500": "^GSPC",
    "asx200": "^AXJO",
}

def fetch_prices():
    results = {}
    for name, ticker in TICKERS.items():
        data = yf.Ticker(ticker).history(period="2d")  # 2 days so we can calc daily change later
        if data.empty:
            results[name] = {"error": f"No data returned for {ticker}"}
            continue

        latest = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else latest

        results[name] = {
            "ticker": ticker,
            "latest_close": round(float(latest["Close"]), 2),
            "previous_close": round(float(previous["Close"]), 2),
            "latest_date": str(data.index[-1].date()),
        }

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "data": results,
    }
    return output

def fetch_and_save():
    output = fetch_prices()
    with open("data/raw_prices.json", "w") as f:
        json.dump(output, f, indent=2)
    return output

if __name__ == "__main__":
    output = fetch_and_save()
    print("Fetch complete. Saved to data/raw_prices.json")
    print(json.dumps(output, indent=2))