import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

NK225_data = yf.download('^N225', start='任意の日付', end=datetime.now().strftime('%Y-%m-%d'))

NK225_prices = NK225_data['Adj Close']

NK225_prices = NK225_prices.dropna()

NK225_prices.to_csv('NK225_prices.csv')

NK225_prices = pd.read_csv('NK225_prices.csv', index_col='Date', parse_dates=True)

X = np.arange(len(NK225_prices)).reshape(-1, 1)  # インデックスを特徴量として使用
y = NK225_prices.values.reshape(-1, 1)  # 終値をターゲットとして使用

regression_model = LinearRegression()
regression_model.fit(X, y)

forecast_days = 30

last_date = NK225_prices.index[-1]
forecast_start_date = last_date + timedelta(days=1)

forecast_dates = pd.date_range(start=forecast_start_date, periods=forecast_days, freq='B')

# 予測対象の特徴量を作成
X_forecast = np.arange(len(NK225_prices), len(NK225_prices) + forecast_days).reshape(-1, 1)

# 予測値を計算
y_forecast = regression_model.predict(X_forecast)

# 予測値の日付と値を結合
forecast_data = pd.DataFrame(y_forecast, index=forecast_dates, columns=['Forecast'])

combined_data = pd.concat([NK225_prices, forecast_data])

# グラフの表示範囲を設定
start_date = datetime(2023, 1, 1)
combined_data = combined_data.loc[start_date:]

# 結果の可視化
plt.figure(figsize=(10, 6))
plt.plot(combined_data.index, combined_data['Adj Close'], color='blue', label='Actual')
plt.plot(combined_data.index, combined_data['Forecast'], color='red', linewidth=2, label='Forecast')
plt.xlabel('Date')
plt.ylabel('NK225 Price')
plt.title('NK225 Price Forecast')
plt.legend()
plt.show()

