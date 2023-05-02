import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline

# 学習用データの読み込み
df_train = pd.read_csv('koukoku_train.csv')

# 検証用データの読み込み
df_test = pd.read_csv('koukoku_test.csv')

df_train.head()


# One hot encoding などで数値に変換する必要がある
x_train = df_train.drop('cv', axis = 1)
y_train = df_train['cv'].map(lambda x: 1 if x =='YES' else 0)
x_test = df_test.drop('cv', axis = 1)
y_test = df_test['cv'].map(lambda x: 1 if x =='YES' else 0)


# 決定木の学習モデルを作成
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth = 3, min_samples_leaf = 1, min_samples_split = 3)
model.fit(x_train, y_train)


# 決定木の学習モデルの可視化
from sklearn.tree import export_graphviz
import pydotplus
from six import StringIO
from IPython.display import Image
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,
               feature_names=x_train.columns,
               class_names=['No', 'Yes'],
               filled = True, rounded=True)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())


# 決定木の各特徴量の重要性を可視化
n_features = len(x_train.columns)
plt.barh(range(n_features), model.feature_importances_, align = 'center')
plt.yticks(np.arange(n_features), x_train.columns)
plt.xlabel('importance')
plt.ylabel('feature')


# 学習モデルの当てはめ値の算出
# 指数表記の禁止
np.set_printoptions(suppress=True)
model.predict_proba(x_test)



#学習モデルを用いた検証用データの分類結果を表示
model.predict(x_test)


# 混同行列（confusion matrix)
from sklearn.metrics import confusion_matrix
print('confusion matrix =')
print(confusion_matrix(y_true = y_test,
                      y_pred = model.predict(x_test)))


# 正解率（accuracy)
# 分類したデータの総数のうち、正しく分類されたデータ数の割合
print('正解率(train):{:.3f}'.format(model.score(x_train, y_train)))
print('正解率(test):{:.3f}'.format(model.score(x_test, y_test)))

# 適合率
from sklearn.metrics import precision_score
print('precision = ', precision_score(y_true = y_test,
                                     y_pred = model.predict(x_test)))

# 再現率
from sklearn.metrics import recall_score
print('recall = ', recall_score(y_true = y_test,
                               y_pred = model.predict(x_test)))


# F1
from sklearn.metrics import f1_score
print('f1 score = ', f1_score(y_true = y_test,
                             y_pred = model.predict(x_test)))


# AUC
from sklearn.metrics import roc_auc_score
print('auc = ', roc_auc_score(y_true = y_test,
                             y_score = model.predict_proba(x_test)[:, 1]))


# ROC曲線
from sklearn.metrics import roc_curve, auc

# 検証データがクラス1に属する確率
y_score = model.predict_proba(x_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_true=y_test, y_score=y_score)

plt.plot(fpr, tpr, label='roc curve (area = %0.3f)' % auc(fpr, tpr))
plt.plot([0, 1], [0, 1], linestyle='--', label='random')
plt.plot([0, 0, 1], [0, 1, 1], linestyle='--', label='ideal')
plt.legend()
plt.xlabel('false positive rate')
plt.ylabel('true positive rate')
plt.show()