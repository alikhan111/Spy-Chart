import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta

# Get yesterday's date
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

# Download SPY 1-minute data for yesterday
data = yf.download("SPY", start=yesterday, end=today, interval="1m")

# Filter only yesterday's data
data = data[data.index.date == yesterday]

if data.empty:
    print(f"No data available for {yesterday}")
else:
    mpf.plot(data, type='candle', style='charles',
             title=f"SPY Chart - {yesterday}",
             volume=True, mav=(9, 21))
