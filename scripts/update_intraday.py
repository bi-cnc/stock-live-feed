import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
import os

TICKERS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
PERIOD = "2d"
INTERVAL = "5m"

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_and_save(ticker):
    try:
        df = yf.download(ticker, period=PERIOD, interval=INTERVAL, auto_adjust=True, progress=False)
        if df.empty:
            print(f"⚠️ No data for {ticker}")
            return
        df = df.reset_index()
        df["Datetime"] = df["Datetime"].dt.tz_convert("Europe/Prague")
        df["Datetime"] = df["Datetime"].dt.strftime("%Y-%m-%d %H:%M")
        df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
        df.to_csv(os.path.join(DATA_DIR, f"{ticker}.csv"), index=False)
        print(f"✅ Saved {ticker}")
    except Exception as e:
        print(f"❌ Error {ticker}: {e}")

def main():
    print(f"=== Update started {datetime.now(timezone.utc)} ===")
    for t in TICKERS:
        fetch_and_save(t)
    print("=== Done ===")

if __name__ == "__main__":
    main()
