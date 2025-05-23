import yfinance as yf
import pandas as pd
import numpy as np
from google.colab import drive
from datetime import datetime
import matplotlib.pyplot as plt
import re
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import lightgbm as lgb


df = yf.download("任意", start="任意", end=datetime.now().strftime('%Y-%m-%d'), group_by='ticker')

if isinstance(df.columns, pd.MultiIndex):
    if '"任意"' in df.columns.levels[0]:
        df = df.xs('"任意"', level=0, axis=1)

if 'Close' not in df.columns and 'Adj Close' in df.columns:
    df['Close'] = df['Adj Close']

df.ffill(inplace=True)

df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day
df['day_of_week'] = df.index.dayofweek
df['day_of_year'] = df.index.dayofyear
df['week_of_year'] = df.index.isocalendar().week.astype(int)

df['lag_1'] = df['Close'].shift(1)
df['lag_7'] = df['Close'].shift(7)
df['lag_14'] = df['Close'].shift(14)
df['lag_30'] = df['Close'].shift(30)

df['roll_mean_7'] = df['Close'].rolling(window=7).mean()
df['roll_mean_14'] = df['Close'].rolling(window=14).mean()
df['roll_mean_30'] = df['Close'].rolling(window=30).mean()

df['roll_std_7'] = df['Close'].rolling(window=7).std()
df['roll_std_14'] = df['Close'].rolling(window=14).std()
df['roll_std_30'] = df['Close'].rolling(window=30).std()

df['return'] = df['Close'].pct_change()
df['volatility_7'] = df['return'].rolling(window=7).std()
df['volatility_14'] = df['return'].rolling(window=14).std()
df['volatility_30'] = df['return'].rolling(window=30).std()

df['target'] = df['Close'].shift(-30)


fx = yf.download(""任意"", start=""任意"", end=datetime.now().strftime('%Y-%m-%d'))
if isinstance(fx.columns, pd.MultiIndex):
    fx.columns = ['_'.join(col).strip() for col in fx.columns.values]

if '"任意"' in fx.columns:
    fx.rename(columns={'"任意"': '"任意"'}, inplace=True)
else:
    raise KeyError("データに '"任意"' カラムが見つかりません。")

fx.ffill(inplace=True)


df = df.join(fx[['"任意"']], how='left')
df.ffill(inplace=True)

# 特徴量リスト拡張
features = [
    'year', 'month', 'day', 'day_of_week', 'day_of_year', 'week_of_year',
    'lag_1', 'lag_7', 'lag_14', 'lag_30',
    'roll_mean_7', 'roll_mean_14', 'roll_mean_30',
    'roll_std_7', 'roll_std_14', 'roll_std_30',
    'volatility_7', 'volatility_14', 'volatility_30',
    '_Close'
]

def clean_column_names(cols):
    return [re.sub(r'[^A-Za-z0-9_]+', '', c) for c in cols]

cleaned_features = clean_column_names(features)
rename_dict = dict(zip(features, cleaned_features))
df.rename(columns=rename_dict, inplace=True)
features = cleaned_features

required_cols = features + ['target']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"以下のカラムが存在しません: {missing_cols}")

df.dropna(subset=required_cols, inplace=True)

split_idx = int(len(df) * 0.8)
train = df.iloc[:split_idx]
test = df.iloc[split_idx:]

X_train = train[features]
y_train = train['target']
X_test = test[features]
y_test = test['target']

def tune_xgb(X, y):
    model = xgb.XGBRegressor(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1]
    }
    grid = GridSearchCV(model, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
    grid.fit(X, y)
    print(f"Best XGB params: {grid.best_params_}")
    return grid.best_estimator_

def tune_lgb(X, y):
    model = lgb.LGBMRegressor(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1]
    }
    grid = GridSearchCV(model, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
    grid.fit(X, y)
    print(f"Best LGB params: {grid.best_params_}")
    return grid.best_estimator_

model_xgb = tune_xgb(X_train, y_train)
pred_xgb = model_xgb.predict(X_test)
rmse_xgb = np.sqrt(mean_squared_error(y_test, pred_xgb))
print(f"XGBoost RMSE: {rmse_xgb:.2f}")

model_lgb = tune_lgb(X_train, y_train)
pred_lgb = model_lgb.predict(X_test)
rmse_lgb = np.sqrt(mean_squared_error(y_test, pred_lgb))
print(f"LightGBM RMSE: {rmse_lgb:.2f}")

plt.figure(figsize=(14, 6))
plt.plot(test.index, y_test, label='Actual', color='black')
plt.plot(test.index, pred_xgb, label='XGBoost', alpha=0.7)
plt.plot(test.index, pred_lgb, label='LightGBM', alpha=0.7)
plt.legend()
plt.title('30-Day Ahead Forecast with ')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.grid()
plt.show()


