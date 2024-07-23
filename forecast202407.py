import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import japanize_matplotlib

def download_data(ticker, start_date, end_date):
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"データが見つかりません: {ticker}")
        return data
    except Exception as e:
        raise RuntimeError(f"データのダウンロード中にエラーが発生しました: {e}")

def preprocess_data(data, column='Adj Close'):
    
    prices = data[column].dropna()
    return np.log(prices)

def split_data(data, train_ratio=0.9):
    
    train_size = int(len(data) * train_ratio)
    return data[:train_size], data[train_size:]

def train_arima_model(train_data):
    
    model = auto_arima(train_data, suppress_warnings=True)
    order = model.order
    arima_model = ARIMA(train_data, order=order)
    return arima_model.fit()

def forecast(model, steps):
    
    forecast_result = model.get_forecast(steps=steps)
    return forecast_result.predicted_mean

def plot_forecast(original_data, train_data, test_data, forecast_values):
    
    plt.figure(figsize=(12, 6))
    plt.plot(np.exp(original_data), label='実際の価格')
    plt.plot(test_data.index, np.exp(forecast_values), label='予測価格', linestyle='--')
    plt.title('任意 Prices Forecast')
    plt.xlabel('日付')
    plt.ylabel('価格')
    plt.legend()
    plt.show()

def main():
    # データ取得
    ticker = '任意'
    start_date = '任意の日付'
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = download_data(ticker, start_date, end_date)
    
    # データ前処理
    log_prices = preprocess_data(data)

    # データ分割
    train_data, test_data = split_data(log_prices)

    # モデルトレーニング
    model = train_arima_model(train_data)

    # 予測
    forecast_values = forecast(model, len(test_data))

    # プロット
    plot_forecast(log_prices, train_data, test_data, forecast_values)

    # 予測値を表示
    print("未来の予測値:")
    print(np.exp(forecast_values))

if __name__ == "__main__":
    main()