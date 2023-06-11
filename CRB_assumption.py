import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# CRB指数構成商品のシンボルリスト
commodity_symbols = ['CL=F', 'GC=F', 'SI=F', 'HG=F', 'NG=F', 'ZW=F', 'ZC=F', 'ZS=F', 'SB=F', 'KC=F']

# 商品価格データの取得
prices = yf.download(commodity_symbols, start='2000-01-01', end=datetime.today().strftime('%Y-%m-%d'))['Adj Close']

# 加重平均を計算
weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 各商品の重み（仮定）
crb_index = (prices * weights).sum(axis=1) / sum(weights)

# グラフの作成
plt.figure(figsize=(10, 6))
plt.plot(crb_index.index, crb_index.values)
plt.title('CRB Index')
plt.xlabel('Date')
plt.ylabel('CRB Index')
plt.grid(True)
plt.show()