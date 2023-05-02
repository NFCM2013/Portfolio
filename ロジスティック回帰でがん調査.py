
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline
from sklearn.datasets import load_breast_cancer

# データセットの読み込み
cancer = load_breast_cancer()

import pandas as pd
# 説明変数(cancer.data)をDataFrameに保存
df = pd.DataFrame(cancer.data, columns = cancer.feature_names)

# 目的変数(cancer.target)もDataFrameに追加
df['type'] = cancer.target 
df.head()


from sklearn.model_selection import train_test_split

# 全ての説明変数を使用
x = df.drop(['type'], axis = 1)
y = df['type']  

# データを学習用と検証用に分割
x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size = 0.7, test_size = 0.3, random_state = 0) 


# 標準化
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(x_train)
x_train_std = sc.transform(x_train)
x_test_std = sc.transform(x_test)


# ロジスティック回帰分析
from sklearn.linear_model import LogisticRegression 
model = LogisticRegression(solver = 'lbfgs', penalty = 'l2', C = 1.0)
model.fit(x_train_std, y_train)

print("coefficient = ", model.coef_)
print("intercept = ", model.intercept_)


# 学習モデルの当てはめ値
# 指数表記の禁止
np.set_printoptions(suppress=True) 
model.predict_proba(x_test_std)


# 検証用データの分類結果
model.predict(x_test_std)


# 混合行列
from sklearn.metrics import confusion_matrix
print('confusion matrix =')
print(confusion_matrix(y_true = y_test, 
                       y_pred = model.predict(x_test_std)))


# 正解率
print('正解率(train):{:.3f}'.format(model.score(x_train_std, y_train)))
print('正解率(test):{:.3f}'.format(model.score(x_test_std, y_test)))


# 適合率
from sklearn.metrics import precision_score
print('precision = ', precision_score(y_true = y_test, 
                                      y_pred = model.predict(x_test_std)))


# 再現率
from sklearn.metrics import recall_score
print('recall = ', recall_score(y_true = y_test, 
                                y_pred = model.predict(x_test_std)))


# F1スコア
from sklearn.metrics import f1_score
print('f1 score = ', f1_score(y_true = y_test, 
                              y_pred = model.predict(x_test_std)))


# AUCスコア
from sklearn.metrics import roc_auc_score
print('auc = ', roc_auc_score(y_true = y_test, 
                              y_score = model.predict_proba(x_test_std)[:, 1]))


# ROC曲線
from sklearn.metrics import roc_curve, auc

y_score = model.predict_proba(x_test_std)[:, 1] # 検証データがクラス1に属する確率
fpr, tpr, thresholds = roc_curve(y_true=y_test, y_score=y_score)

plt.plot(fpr, tpr, label='roc curve (area = %0.3f)' % auc(fpr, tpr))
plt.plot([0, 1], [0, 1], linestyle='--', label='random')
plt.plot([0, 0, 1], [0, 1, 1], linestyle='--', label='ideal')
plt.legend()
plt.xlabel('false positive rate')
plt.ylabel('true positive rate')
plt.show()


