import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 株価指数のシンボル
symbols = ['^N225', '^GSPC', '^FTSE', '^GDAXI', '^FCHI', '^HSI']

# 2023年1月1日から今日までの株価データを取得
start_date = '2023-01-01'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# 株価データを格納するDataFrameを作成
df_prices = pd.DataFrame()

# 株価データの取得とDataFrameへの追加
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date)
    df_prices[symbol] = data['Close']

# CSVファイルに株価データを保存
df_prices.to_csv('stock_prices.csv')

# CSVファイルから株価データを読み込み
df_prices = pd.read_csv('stock_prices.csv', index_col=0, parse_dates=True)

# スタート地点の価格に対する株価指数のパフォーマンスを計算
start_prices = df_prices.iloc[0]
df_performance = df_prices.divide(start_prices).multiply(100)

# グラフの作成
plt.figure(figsize=(12, 6))

for symbol in symbols:
    plt.plot(df_performance.index, df_performance[symbol], label=symbol)

plt.xlabel('Date')
plt.ylabel('Performance (%)')
plt.title('Stock Performance in 2023')
plt.legend()
plt.grid(True)
plt.show()