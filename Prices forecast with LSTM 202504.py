import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import japanize_matplotlib

def download_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"データが見つかりません: {ticker}")

        
        if 'Adj Close' not in data.columns:
            print("警告: 'Adj Close' が見つからないため、'Close' を使用します。")
            return data[['Close']]
        return data[['Adj Close']]
    except Exception as e:
        raise RuntimeError(f"データのダウンロード中にエラーが発生しました: {e}")

def preprocess_data(data, column='Close'):  # 'Adj Close' を 'Close' に変更
    prices = data[column].dropna().values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(prices)
    return scaled_data, scaler

def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def evaluate_forecast(test_data, predicted_values):
    rmse = np.sqrt(mean_squared_error(test_data, predicted_values))
    mae = mean_absolute_error(test_data, predicted_values)
    r2 = r2_score(test_data, predicted_values)
    return rmse, mae, r2

def plot_forecast(original_data, train_data, test_data, predicted_values, forecast_values, train_dates, test_dates, forecast_dates):
    plt.figure(figsize=(12, 6))
    plt.plot(train_dates, train_data, label='トレーニングデータ', color='blue')
    plt.plot(test_dates, test_data, label='実際の価格', color='green')
    plt.plot(test_dates, predicted_values, label='予測価格', linestyle='--', color='red')
    plt.plot(forecast_dates, forecast_values, label='半年後の予測価格', linestyle='--', color='orange')

    plt.title('Prices Forecast with LSTM (半年後予測)')
    plt.xlabel('日付')
    plt.ylabel('価格')
    plt.legend()
    plt.show()

def main():
    ticker = '任意'
    start_date = '任意'
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = download_data(ticker, start_date, end_date)

    scaled_data, scaler = preprocess_data(data)

    train_size = int(len(scaled_data) * 0.7) 
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]

    # 日付データの準備
    train_dates = data.index[:train_size]
    test_dates = data.index[train_size:]

    # データセットの作成
    time_step = 60
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=10, batch_size=64, verbose=1)

    # テストデータの予測
    predicted_test = model.predict(X_test)

    # スケールを元に戻す
    predicted_test = scaler.inverse_transform(predicted_test)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

    future_steps = 180
    last_data = scaled_data[-time_step:].reshape(1, -1, 1)
    forecast_values = []

    for _ in range(future_steps):
        predicted_value = model.predict(last_data)
        forecast_values.append(predicted_value[0, 0])
        last_data = np.append(last_data[:, 1:, :], predicted_value.reshape(1, 1, 1), axis=1)

    forecast_values = scaler.inverse_transform(np.array(forecast_values).reshape(-1, 1))

    # 予測評価
    rmse, mae, r2 = evaluate_forecast(y_test, predicted_test)
    print(f"RMSE: {rmse}, MAE: {mae}, R2: {r2}")

    # 未来の日付の作成
    last_test_date = test_dates[-1]
    forecast_dates = pd.date_range(last_test_date + timedelta(days=1), periods=future_steps, freq='B')

    # プロット
    plot_forecast(data['Close'].values,
                   scaler.inverse_transform(train_data[time_step:]),
                   y_test,
                   predicted_test,
                   forecast_values,
                   train_dates[time_step:],
                   test_dates[time_step:],
                   forecast_dates)

if __name__ == "__main__":
    main()