# filename: plot_stock_prices.py

import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbols and the start date for YTD
symbols = ['NVDA', 'TSLA']
start_date = '2025-01-01'

# Download the stock data
data = yf.download(symbols, start=start_date)

# Plot the adjusted closing prices for NVDA and TSLA
plt.figure(figsize=(10, 6))
plt.plot(data['Adj Close']['NVDA'], label='NVDA Stock Price (YTD)', color='blue')
plt.plot(data['Adj Close']['TSLA'], label='TSLA Stock Price (YTD)', color='red')

# Add labels and title
plt.title('Stock Price Change YTD: NVDA vs TSLA')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()