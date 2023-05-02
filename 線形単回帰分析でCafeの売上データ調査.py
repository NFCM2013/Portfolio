import pandas as pd
import numpy as np

# データの読み込み
df_train = pd.read_csv('icecoffee_train.csv')
df_train.head()

df_test = pd.read_csv('icecoffee_test.csv')
df_test.head()


# 売り上げデータに対する線形単回帰分析
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')

x_train = df_train['temperature']
y_train = df_train['icecoffee']

# 学習用データの気温とアイスコーヒーの売り上げの散布図をプロット
plt.scatter(x_train, y_train)
plt.title('Scatter Plot of temperature vs icecoffee_train')
plt.xlabel('temperature')
plt.ylabel('icecoffee')
plt.grid()
plt.show()


x_test = df_test['temperature']
y_test = df_test['icecoffee']

# 検証用データの気温とアイスコーヒーの売り上げの散布図をプロット
plt.scatter(x_test, y_test)
plt.title('Scatter Plot of temperature vs icecoffee_test')
plt.xlabel('temperature')
plt.ylabel('icecoffee')
plt.grid()
plt.show()


# 学習用データと検証用データの気温とアイスコーヒーの売り上げの散布図をプロット
fig, ax = plt.subplots()
ax.scatter(x_train, y_train, color = 'blue', label = 'train')
ax.scatter(x_test, y_test, color = 'black', label = 'test')
plt.legend()
plt.title('Correlation')
plt.xlabel('temperature')
plt.ylabel('icecoffee')
plt.show()


# 相関係数の確認
print(df_train[['temperature', 'icecoffee']].corr())
print(df_test[['temperature', 'icecoffee']].corr())


# 回帰式の算出
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline


# 線形多項式回帰モデルの生成
x_train = np.array(x_train).reshape(-1, 1) 
y_train = np.array(y_train)

# 次数 = 1（線形単回帰）
model_1 = Pipeline([
    ('poly', PolynomialFeatures(degree=1)),
    ('linear', LinearRegression())
])

model_1.fit(x_train, y_train)

# 次数 = 2

model_2 = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression())
])
model_2.fit(x_train, y_train)

# 次数 = 3

model_3 = Pipeline([
    ('poly', PolynomialFeatures(degree=3)),
    ('linear', LinearRegression())
])

model_3.fit(x_train, y_train)

# 次数 = 4

model_4 = Pipeline([
    ('poly', PolynomialFeatures(degree=4)),
    ('linear', LinearRegression())
])

model_4.fit(x_train, y_train)


# 回帰モデルのグラフ化
fig, ax = plt.subplots()
ax.scatter(x_train, y_train, color = 'blue')

_x = np.linspace(24, 35, 100).reshape(-1, 1)
plt.plot(_x, model_1.predict(_x), color = 'red', label = 'degree = 1')
plt.plot(_x, model_2.predict(_x), color = 'green', label = 'degree = 2')
plt.plot(_x, model_3.predict(_x), color = 'yellow', label = 'degree = 3')
plt.plot(_x, model_4.predict(_x), color = 'purple', label = 'degree = 4')

plt.legend()
plt.title('Regression Line')
plt.xlabel('x')
plt.ylabel('y')
plt.show()