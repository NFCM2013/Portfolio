import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
from datetime import datetime

# 株価指数のシンボルリスト
index_symbols = ['^GSPC', '^IXIC', '^FTSE', '^GDAXI', '^FCHI', '^N225']

# 株価データの取得
stock_data = yf.download(index_symbols, start='2000-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# 終値データの取得
close_prices = stock_data['Close']

# RSIの計算
rsi_data = close_prices.apply(lambda x: talib.RSI(np.array(x)))

# グラフの作成
plt.figure(figsize=(10, 6))
for symbol in index_symbols:
    plt.plot(stock_data.index, rsi_data[symbol], label=symbol)
plt.title('RSI of Major Stock Indices')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()
plt.grid(True)
plt.show()