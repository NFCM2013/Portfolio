import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

symbols_with_names = {
    '1775.T': 'Fuji Furukawa Engineering & Construction Co., Ltd.',
    '3186.T': 'NEXTAGE Co., Ltd.',
    '3231.T': 'Nomura Real Estate',
    '3360.T': 'Ship Healthcare Holdings, Inc.',
    '4528.T': 'Ono Pharmaceutical Co., Ltd.',
    '5310.T': 'Toyo Tanso Co., Ltd.',
    '5423.T': 'Tokyo Steel Manufacturing Co., Ltd.',
    '5706.T': 'Mitsui Mining and Smelting Co., Ltd.',
    '5715.T': 'Furukawa Co Ltd',
    '5803.T': 'Fujikura Ltd.',
    '6023.T': 'Daihatsu Diesel Mfg Co., Ltd.',
    '6196.T': 'Strike Co., Ltd.',
    '6454.T': 'Max Co., Ltd.',
    '7818.T': 'Transaction Co., Ltd.',
    '9161.T': 'ID＆E HLDG.',
    '9432.T': 'NTT',
    '9433.T': 'KDDI',
    '9928.T': 'Miroku Jyoho Service Co., Ltd.'
}

start_date = '任意'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')


df_prices = pd.DataFrame()

for symbol, name in symbols_with_names.items():
    print(f"Fetching data for {symbol} ({name})...")
    data = yf.download(symbol, start=start_date, end=end_date)
    if not data.empty:
        df_prices[symbol] = data['Close']

df_prices.fillna(method='ffill', inplace=True)
df_prices.fillna(method='bfill', inplace=True)

start_prices = df_prices.iloc[0]
end_prices = df_prices.iloc[-1]
df_performance = df_prices.divide(start_prices).multiply(100)

performance = ((end_prices - start_prices) / start_prices) * 100

print("\n=== Final Performance of Stocks ===")
for symbol, name in symbols_with_names.items():
    if symbol in performance:
        performance_value = performance[symbol]
        sign = "-" if performance_value < 0 else "+"
        print(f"{name} ({symbol}): {sign}{abs(performance_value):.2f}%")

num_colors = len(symbols_with_names)
cmap = cm.get_cmap('tab20', num_colors)
colors = [cmap(i) for i in range(num_colors)]

line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X']

plt.figure(figsize=(14, 8))
for i, (symbol, name) in enumerate(symbols_with_names.items()):
    color = colors[i]
    line_style = line_styles[i % len(line_styles)]
    marker = markers[i % len(markers)]
    plt.plot(
        df_performance.index,
        df_performance[symbol],
        label=f"{name} ({symbol})",
        color=color,
        linestyle=line_style,
        marker=marker,
        markersize=6
    )
    performance_value = performance[symbol]
    sign = "-" if performance_value < 0 else "+"
    plt.text(
        df_performance.index[-1], df_performance[symbol].iloc[-1],
        f"{sign}{abs(performance_value):.2f}%",
        fontsize=8,
        color=color
    )


plt.xlabel('Date')
plt.ylabel('Performance (%)')
plt.title('Stock Performance')
plt.legend(loc='upper left', fontsize=8, ncol=2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


