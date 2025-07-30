import yfinance as yf
import json
import os
import subprocess
from datetime import datetime


def fetch_and_save_json():
    # Fetch 5-min Nifty 50 data for the last 1 day
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d", interval="5m")
    data.dropna(inplace=True)

    # Format for frontend
    formatted_data = {
        "timestamp": [int(d.timestamp()) for d in data.index],
        "indicators": {
            "quote": [{
                "open": data["Open"].round(2).tolist(),
                "high": data["High"].round(2).tolist(),
                "low": data["Low"].round(2).tolist(),
                "close": data["Close"].round(2).tolist()
            }]
        }
    }

    with open("nifty_5min.json", "w") as f:
        json.dump(formatted_data, f, indent=2)

    print(f"[{datetime.now()}] ✅ JSON file 'nifty_5min.json' updated.")


def git_push():
    try:
        # Skip JSON if it's ignored; commit only .py or required files
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto update: {datetime.now()}"], check=True)
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("📤 Code pushed to GitHub (excluding ignored files).")
    except subprocess.CalledProcessError as e:
        print("❌ Git push failed:", e)


if __name__ == "__main__":
    fetch_and_save_json()
    if os.path.isdir(".git"):
        git_push()
    else:
        print("⚠️ Not a Git repo. Commit skipped.")
