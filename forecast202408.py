import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
import japanize_matplotlib

def download_data(ticker, start_date, end_date):
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"データが見つかりません: {ticker}")
        return data
    except Exception as e:
        raise RuntimeError(f"データのダウンロード中にエラーが発生しました: {e}")
    
# データの前処理
def preprocess_data(data, column='Adj Close'):
    
    prices = data[column].dropna()
    return np.log(prices)

def split_data(data, train_ratio=0.9):
    
    train_size = int(len(data) * train_ratio)
    return data[:train_size], data[train_size:]

def train_arima_model(train_data, seasonal=False, m=1):
    try:
        model = auto_arima(train_data, seasonal=seasonal, m=m, suppress_warnings=True, error_action='ignore')
        order = model.order
        arima_model = ARIMA(train_data, order=order)
        return arima_model.fit()
    except Exception as e:
        raise RuntimeError(f"ARIMAモデルのトレーニング中にエラーが発生しました: {e}")

def forecast(model, steps):
    
    forecast_result = model.get_forecast(steps=steps)
    return forecast_result.predicted_mean, forecast_result.conf_int()

def evaluate_forecast(test_data, forecast_values):
    
    rmse = np.sqrt(mean_squared_error(np.exp(test_data), np.exp(forecast_values)))
    mae = mean_absolute_error(np.exp(test_data), np.exp(forecast_values))
    return rmse, mae

def plot_forecast(original_data, train_data, test_data, forecast_values, conf_int):
    plt.figure(figsize=(12, 6))
    plt.plot(np.exp(original_data), label='実際の価格')
    plt.plot(test_data.index, np.exp(forecast_values), label='予測価格', linestyle='--')
    plt.fill_between(test_data.index, np.exp(conf_int.iloc[:, 0]), np.exp(conf_int.iloc[:, 1]), color='pink', alpha=0.3, label='信頼区間')
    plt.title('Prices Forecast')
    plt.xlabel('日付')
    plt.ylabel('価格')
    plt.legend()
    plt.show()

def main():
    ticker = '任意'
    start_date = '任意の日付'
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = download_data(ticker, start_date, end_date)

    log_prices = preprocess_data(data)

    train_data, test_data = split_data(log_prices)

    # モデルトレーニング
    model = train_arima_model(train_data)

    # 予測
    forecast_values, conf_int = forecast(model, len(test_data))

    # 予測評価
    rmse, mae = evaluate_forecast(test_data, forecast_values)
    print(f"RMSE: {rmse}, MAE: {mae}")

    plot_forecast(log_prices, train_data, test_data, forecast_values, conf_int)

    print("未来の予測値:")
    print(np.exp(forecast_values))

if __name__ == "__main__":
    main()