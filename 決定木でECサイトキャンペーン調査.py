import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline

df_train = pd.read_csv('retention_train.csv')
df_test = pd.read_csv('retention_test.csv')
df_train.head()


# One hot encoding
x_train = df_train.drop('retention', axis = 1)
y_train = df_train['retention'].map(lambda x: 1 if x == 'Yes' else 0)
x_test = df_test.drop('retention', axis = 1)
y_test = df_test['retention'].map(lambda x: 1 if x == 'Yes' else 0)


# 決定木の学習モデルを作成
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(x_train, y_train)


# 決定木の学習モデルの可視化
from sklearn.tree import export_graphviz
import pydotplus
from six import StringIO
from IPython.display import Image

dot_data = StringIO()
export_graphviz(model, out_file=dot_data, feature_names=x_train.columns, class_names=['No', 'Yes'], filled=True, rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())


# 決定木の各特徴量の重要性を可視化
n_features = len(x_train.columns)
plt.barh(range(n_features), model.feature_importances_, align = 'center')
plt.yticks(np.arange(n_features), x_train.columns)
plt.xlabel('importance')
plt.ylabel('feature')


