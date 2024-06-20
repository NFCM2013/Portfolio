import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

NK225_data = yf.download('^N225', start='任意の日付', end=datetime.now().strftime('%Y-%m-%d'))
NK225_prices = NK225_data['Adj Close'].dropna()

NK225_prices = pd.DataFrame(NK225_prices)
NK225_prices['SMA_20'] = NK225_prices['Adj Close'].rolling(window=20).mean()
NK225_prices['SMA_50'] = NK225_prices['Adj Close'].rolling(window=50).mean()
NK225_prices['Volatility'] = NK225_prices['Adj Close'].rolling(window=20).std()
NK225_prices = NK225_prices.dropna()

for lag in range(1, 6):
    NK225_prices[f'Lag_{lag}'] = NK225_prices['Adj Close'].shift(lag)
NK225_prices = NK225_prices.dropna()

X = NK225_prices.drop(['Adj Close'], axis=1).values
y = NK225_prices['Adj Close'].values

scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, shuffle=False)

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3)
grid_search.fit(X_train, y_train.ravel())

best_model = grid_search.best_estimator_

y_pred_scaled = best_model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
y_test = scaler_y.inverse_transform(y_test)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse}, MAE: {mae}, R2: {r2}')

forecast_days = 30
last_date = NK225_prices.index[-1]
forecast_start_date = last_date + timedelta(days=1)
forecast_dates = pd.date_range(start=forecast_start_date, periods=forecast_days, freq='B')

last_data = NK225_prices.iloc[-1].drop('Adj Close')
X_forecast = [last_data.values]
for _ in range(forecast_days - 1):
    pred = best_model.predict(scaler_X.transform(X_forecast[-1].reshape(1, -1)))
    pred = scaler_y.inverse_transform(pred.reshape(-1, 1))
    next_data = np.append(X_forecast[-1][1:], pred[0])
    X_forecast.append(next_data)
X_forecast = np.array(X_forecast)

y_forecast = best_model.predict(scaler_X.transform(X_forecast))
y_forecast = scaler_y.inverse_transform(y_forecast.reshape(-1, 1))

forecast_data = pd.DataFrame(y_forecast, index=forecast_dates, columns=['Forecast'])
combined_data = pd.concat([NK225_prices['Adj Close'], forecast_data], axis=1)

start_date = datetime(2023, 1, 1)
combined_data = combined_data.loc[start_date:]

plt.figure(figsize=(10, 6))
plt.plot(combined_data.index, combined_data['Adj Close'], color='blue', label='Actual')
plt.plot(combined_data.index, combined_data['Forecast'], color='red', linewidth=2, label='Forecast')
plt.xlabel('Date')
plt.ylabel('NK225 Price')
plt.title('NK225 Price Forecast with Random Forest')
plt.legend()
plt.show()