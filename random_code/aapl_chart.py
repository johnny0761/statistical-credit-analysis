import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the ticker and time range
ticker = 'AAPL'
end_date = datetime.today()
start_date = end_date - timedelta(days=180)

# Download historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Plot the closing price
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'], label='AAPL Close Price')
plt.title('AAPL Stock Price - Last 6 Months')
plt.xlabel('Date')
plt.ylabel('Close Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
