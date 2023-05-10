! pip install yfinance
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# fibbonacchi retracementを計算する関数
def calc_fibonacci_retracement(df, trend_direction):
    top = df['Close'].max()
    bottom = df['Close'].min()
    diff = top - bottom
    
    if trend_direction == 'upward':
        first_level = top - diff * 0.236
        second_level = top - diff * 0.382
        third_level = top - diff * 0.5
        fourth_level = top - diff * 0.618
        fifth_level = top - diff * 0.764
    elif trend_direction == 'downward':
        first_level = bottom + diff * 0.236
        second_level = bottom + diff * 0.382
        third_level = bottom + diff * 0.5
        fourth_level = bottom + diff * 0.618
        fifth_level = bottom + diff *0.764
    
    return top, bottom, first_level, second_level, third_level, fourth_level, fifth_level

# 株価情報を取得
symbol = 'AAPL' # Appleの株価情報を取得する例
stock_data = yf.download(symbol, period="max")

# fibbonacchi retracementを計算
top, bottom, first_level, second_level, third_level, fourth_level, fifth_level = calc_fibonacci_retracement(stock_data, 'upward')

# チャートをプロット
plt.plot(stock_data['Close'], label="Stock Price")
plt.axhline(y=top, linestyle="--", color="red", label="Top")
plt.axhline(y=bottom, linestyle="--", color="green", label="Bottom")
plt.axhline(y=first_level, linestyle="--", color="blue", label="23.6%")
plt.axhline(y=second_level, linestyle="--", color="orange", label="38.2%")
plt.axhline(y=third_level, linestyle="--", color="purple", label="50.0%")
plt.axhline(y=fourth_level, linestyle="--", color="brown", label="61.8%")
plt.axhline(y=fifth_level, linestyle="--", color="gray", label="76.4%")
plt.legend(loc="upper left")
plt.show()