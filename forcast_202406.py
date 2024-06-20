import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

NK225_data = yf.download('^N225', start='任意の日付', end=datetime.now().strftime('%Y-%m-%d'))
NK225_prices = NK225_data['Adj Close'].dropna()

NK225_prices.to_csv('NK225_prices.csv')
NK225_prices = pd.read_csv('NK225_prices.csv', index_col='Date', parse_dates=True)

X = np.arange(len(NK225_prices)).reshape(-1, 1)
y = NK225_prices.values.reshape(-1, 1)

scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, shuffle=False)

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3)
grid_search.fit(X_train, y_train.ravel())

best_model = grid_search.best_estimator_

forecast_days = 30
last_date = NK225_prices.index[-1]
forecast_start_date = last_date + timedelta(days=1)
forecast_dates = pd.date_range(start=forecast_start_date, periods=forecast_days, freq='B')

X_forecast = np.arange(len(NK225_prices), len(NK225_prices) + forecast_days).reshape(-1, 1)
X_forecast_scaled = scaler_X.transform(X_forecast)
y_forecast_scaled = best_model.predict(X_forecast_scaled)
y_forecast = scaler_y.inverse_transform(y_forecast_scaled.reshape(-1, 1))

forecast_data = pd.DataFrame(y_forecast, index=forecast_dates, columns=['Forecast'])
combined_data = pd.concat([NK225_prices, forecast_data])

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
