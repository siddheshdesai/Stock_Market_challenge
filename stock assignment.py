import requests
import pandas as pd
from collections import defaultdict

# ----------- Task 1: Fetch Nifty 50 Stocks -----------------

headers = {
    "User-Agent": "Mozilla/5.0"
}

nifty_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
sess = requests.Session()
sess.get("https://www.nseindia.com", headers=headers)

data = sess.get(nifty_url, headers=headers).json()

nifty_symbols = [stock["symbol"] for stock in data["data"]]
print("Nifty 50 Symbols:", nifty_symbols)


# ----------- Task 2: Sector Momentum Analysis -----------------

sector_map = {}
sector_url = "https://www.nseindia.com/api/quote-equity?symbol="

intraday_changes = {}
sectors = defaultdict(list)

for symbol in nifty_symbols:
    try:
        quote = sess.get(sector_url + symbol, headers=headers).json()

        open_price = quote["priceInfo"]["open"]
        current_price = quote["priceInfo"]["lastPrice"]
        sector = quote["industryInfo"]["industry"]

        if open_price and current_price:
            change = ((current_price - open_price) / open_price) * 100
            intraday_changes[symbol] = change
            sectors[sector].append(change)

        print(f"{symbol}: {change:.2f}% | Sector: {sector}")

    except:
        print(f"Skipped {symbol} due to missing data")


# ----------- Sector-wise Average Change -----------------

sector_momentum = {
    sector: sum(values) / len(values)
    for sector, values in sectors.items()
}

# Sort sectors by momentum (descending)
sorted_momentum = dict(sorted(sector_momentum.items(), key=lambda x: x[1], reverse=True))

print("\n\n------ Sector Momentum (Highest → Lowest) ------")
for sector, avg_change in sorted_momentum.items():
    print(f"{sector}: {avg_change:.2f}%")

