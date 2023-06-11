import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


# VIX指数の取得
vix_data = yf.download('^VIX', start='2000-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# 終値データの取得
close_prices = vix_data['Close']

# グラフの作成
plt.figure(figsize=(10, 6))
plt.plot(close_prices)
plt.title('VIX Index (PreFC)')
plt.xlabel('Date')
plt.ylabel('VIX Index')
plt.grid(True)
plt.show()