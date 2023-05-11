import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

# S&P500の株価データを読み込む
sp500 = pd.read_csv('任意のデータ', index_col=0, parse_dates=True)

# 特徴量とターゲット変数を設定する
X = sp500[['Open', 'Volume']]
y = sp500['Close']

# データを訓練用とテスト用に分割する
train_size = int(len(sp500) * 0.7)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 回帰モデルを構築する
model = LinearRegression()
model.fit(X_train, y_train)

# 訓練データとテストデータの予測値を取得する
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# 訓練データとテストデータの性能を評価する
print('MSE (train): %.2f' % mean_squared_error(y_train, y_train_pred))
print('MSE (test): %.2f' % mean_squared_error(y_test, y_test_pred))
print('R2 (train): %.2f' % r2_score(y_train, y_train_pred))
print('R2 (test): %.2f' % r2_score(y_test, y_test_pred))

# 実際の株価と予測値を比較する
plt.plot(sp500.index[train_size:], y_test.values, label='Actual')
plt.plot(sp500.index[train_size:], y_test_pred, label='Predicted')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()