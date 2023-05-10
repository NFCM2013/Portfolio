import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルからデータを読み込む
df = pd.read_csv('任意期間、任意ペアファイル', index_col='Date', parse_dates=True)

# 移動平均を計算する
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# ボリンジャーバンドを計算する
std = df['Close'].rolling(window=20).std()
df['UpperBand'] = df['MA20'] + (2 * std)
df['LowerBand'] = df['MA20'] - (2 * std)

# データを可視化する
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['Close'], label='Close')
ax.plot(df['MA20'], label='MA20')
ax.plot(df['MA50'], label='MA50')
ax.fill_between(df.index, df['UpperBand'], df['LowerBand'], alpha=0.1)
ax.legend(loc='upper left')
ax.set_title('任意通貨ペア Exchange Rate')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
plt.show()

# 統計情報を表示する
print(df.describe())
