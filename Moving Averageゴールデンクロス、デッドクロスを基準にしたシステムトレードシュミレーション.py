# TA-Libのインストール

!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
!tar -xzvf ta-lib-0.4.0-src.tar.gz
!cd ta-lib && ./configure --prefix=/usr && make && make install
!pip install Ta-Lib


import pandas_datareader as pdr
import talib
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# 通貨ペアを指定
pair = 'USDJPY'

# データの期間を指定
start_date = '2000-01-01'
end_date = '2023-03-28'

# Yahoo Financeから為替レートデータを取得
df = yf.download("USDJPY=X", start=start_date, end=end_date)

# 移動平均を計算
ma_fast = talib.SMA(df['Close'], timeperiod=50)
ma_slow = talib.SMA(df['Close'], timeperiod=200)

# ゴールデンクロス、デッドクロスのシグナルを作成
signals = pd.DataFrame(index=df.index)
signals['signal'] = 0.0
signals['signal'][50:] = np.where(ma_fast[50:] > ma_slow[50:], 1.0, 0.0)
signals['positions'] = signals['signal'].diff()

# トレードをシミュレーション
initial_capital = 100000.0
positions = pd.DataFrame(index=signals.index).fillna(0.0)
positions[pair] = 1000 * signals['signal']
portfolio = positions.multiply(df['Close'], axis=0)
pos_diff = positions.diff()
portfolio['holdings'] = (positions.multiply(df['Close'], axis=0)).sum(axis=1)
portfolio['cash'] = initial_capital - (pos_diff.multiply(df['Close'], axis=0)).sum(axis=1).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']
portfolio['returns'] = portfolio['total'].pct_change()

# シグナルとトレードの結果をプロット
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(111, ylabel='Price in $')
df['Close'].plot(ax=ax1, color='black', lw=2.)
ma_fast.plot(ax=ax1, color='red', lw=2.)
ma_slow.plot(ax=ax1, color='blue', lw=2.)
ax1.plot(signals.loc[signals.positions == 1.0].index, df['Close'][signals.positions == 1.0], '^', markersize=10, color='g')
ax1.plot(signals.loc[signals.positions == -1.0].index, df['Close'][signals.positions == -1.0], 'v', markersize=10, color='r')
plt.show()


