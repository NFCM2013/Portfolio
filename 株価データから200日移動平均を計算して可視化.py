import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルからデータを読み込み
symbol_data = pd.read_csv('SP500_stock_data.csv', index_col=0, parse_dates=True)

# 200日移動平均を計算
symbol_data['MA200'] = symbol_data['Close'].rolling(window=200).mean()

# チャートを作成
fig, ax = plt.subplots(figsize=(15,8))
ax.plot(symbol_data['Close'], label='Close')
ax.plot(symbol_data['MA200'], label='MA200')
ax.set_title('S&P 500 Stock Data')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
plt.show()