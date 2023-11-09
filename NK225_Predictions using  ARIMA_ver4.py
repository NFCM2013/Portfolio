import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters
import japanize_matplotlib

# yfinanceを使用して日経225のデータを取得
NK225_data = yf.download('^N225', start='任意の日付', end=datetime.now().strftime('%Y-%m-%d'))

# 'Adj Close'列のデータを取得
NK225_prices = NK225_data['Adj Close']

# 欠損値を削除
NK225_prices = NK225_prices.dropna()

# データをCSVファイルに保存
NK225_prices.to_csv('NK225_prices.csv')

# CSVファイルからデータを読み込む
NK225_prices = pd.read_csv('NK225_prices.csv', index_col='Date', parse_dates=True)

# データの前処理: 対数変換
log_prices = np.log(NK225_prices)

# データをトレーニングデータとテストデータに分割
train_size = int(len(log_prices) * 0.9)
train, test = log_prices[:train_size], log_prices[train_size:]

# ARIMAモデルの次数を自動で選択
model = auto_arima(train, suppress_warnings=True)
order = model.get_params()['order']

# ARIMAモデルの作成とトレーニング
model = ARIMA(train, order=order)
result = model.fit()

# 未来の日付に対する予測
forecast_steps = len(test)
forecast = result.get_forecast(steps=forecast_steps)
forecast_values = np.exp(forecast.predicted_mean)  # 対数変換を元に戻す

# グラフの作成
plt.figure(figsize=(12, 6))
plt.plot(NK225_prices, label='実際の価格')
plt.plot(test.index, forecast_values, label='予測価格', linestyle='--')
plt.title('NK225 Prices Forecast')
plt.xlabel('日付')
plt.ylabel('価格')
plt.legend()
plt.show()

print("未来の予測値:")
print(forecast_values)