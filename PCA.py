# データの読み込み

import pandas as pd

df = pd.read_csv('wine.csv')
df


# 主成分分析の実施

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA()
pca.fit(df)
feature = pca.transform(df)


# 主成分得点
# 各データの主成分得点を表示

pd.DataFrame(feature, columns=['PC{}'.format(x + 1) for x in range(len(df.columns))])


# 主成分分析の結果の確認

import numpy as np

pd.DataFrame(np.round(pca.components_.T, 3),
            index = df.columns,
            columns = ['PC{}'.format(x + 1) for x in range(len(df.columns))])


# 主成分成分の寄与度を可視化
# 第一主成分と第二主成分における観測変数の寄与度を可視化
plt.figure(figsize=(6, 6))

for x, y, name in zip(pca.components_[0], pca.components_[1], df.columns[0:]):
    plt.text(x, y, name)
    
plt.scatter(pca.components_[0], pca.components_[1], alpha=0.8)
plt.grid()
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()


# 主成分分析の累積寄与率を確認
pd.DataFrame(pca.explained_variance_ratio_,
            index=['PC{}'. format(x + 1) for x in range(len(df.columns))])


# 累積寄与率の可視化

import matplotlib.ticker as ticker
plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
plt.plot([0] + list(np.cumsum(pca.explained_variance_ratio_)), '-o')
plt.xlabel('Number of principal components')
plt.ylabel('Cumulative contribution rate')
plt.grid()
plt.show()
