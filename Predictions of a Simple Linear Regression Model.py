import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# yfinanceを使用して任意のデータを取得
gold_data = yf.download('GC=F', start='任意の日付', end=datetime.now().strftime('%Y-%m-%d'))

# 'Adj Close'列のデータを取得
gold_prices = gold_data['Adj Close']

# 欠損値を削除
gold_prices = gold_prices.dropna()

# データをCSVファイルに保存
gold_prices.to_csv('gold_prices.csv')

# CSVファイルからデータを読み込む
gold_prices = pd.read_csv('gold_prices.csv', index_col='Date', parse_dates=True)

# 特徴量とターゲットを定義
X = np.arange(len(gold_prices)).reshape(-1, 1)  # インデックスを特徴量として使用
y = gold_prices.values.reshape(-1, 1)  # ゴールドの終値をターゲットとして使用

# 線形回帰モデルを作成して学習
regression_model = LinearRegression()
regression_model.fit(X, y)

# 予測する日数を定義
forecast_days = 30

# 予測対象の日付を取得
last_date = gold_prices.index[-1]
forecast_start_date = last_date + timedelta(days=1)

# 予測する日数分の日付を作成
forecast_dates = pd.date_range(start=forecast_start_date, periods=forecast_days, freq='B')

# 予測対象の特徴量を作成
X_forecast = np.arange(len(gold_prices), len(gold_prices) + forecast_days).reshape(-1, 1)

# 予測値を計算
y_forecast = regression_model.predict(X_forecast)

# 予測値の日付と値を結合
forecast_data = pd.DataFrame(y_forecast, index=forecast_dates, columns=['Forecast'])

# 全体のデータと予測データを結合
combined_data = pd.concat([gold_prices, forecast_data])

# グラフの表示範囲を設定
start_date = datetime(2023, 1, 1)
combined_data = combined_data.loc[start_date:]

# 結果の可視化
plt.figure(figsize=(10, 6))
plt.plot(combined_data.index, combined_data['Adj Close'], color='blue', label='Actual')
plt.plot(combined_data.index, combined_data['Forecast'], color='red', linewidth=2, label='Forecast')
plt.xlabel('Date')
plt.ylabel('Gold Price')
plt.title('Gold Price Forecast')
plt.legend()
plt.show()