import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

symbols_with_names = {
    '2175.T': 'SMS Co., Ltd.',
    '2201.T': 'Morinaga Co., Ltd.',
    '2317.T': 'Systena Corp',
    '2413.T': 'M3 Inc',
    '3186.T': 'NEXTAGE Co., Ltd.',
    '3231.T': 'Nomura Real Estate',
    '4373.T': 'Simplex Holdings, Inc.',
    '4528.T': 'Ono Pharmaceutical Co., Ltd.',
    '4966.T': 'C.Uyemura Co., Ltd.',
    '5423.T': 'Tokyo Steel Manufacturing Co., Ltd.',
    '6013.T': 'Takuma Co., Ltd.',
    '6080.T': 'M&A Capital Partners Co., Ltd.',
    '6101.T': 'Tsugami Corp',
    '6196.T': 'Strike Co., Ltd.',
    '7512.T': 'Aeon Hokkaido Corp',
    '7818.T': 'Transaction Co., Ltd.',
    '7826.T': 'Furuya Metal Co., Ltd.',
    '9161.T': 'ID＆E HLDG.',
    '9432.T': 'NTT Corp',
    '9928.T': 'Miroku Jyoho Service Co., Ltd.'
                
}



start_date = '任意'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')


df_prices = pd.DataFrame()

# 株価データの取得
for symbol, name in symbols_with_names.items():
    print(f"Fetching data for {symbol} ({name})...")
    data = yf.download(symbol, start=start_date, end=end_date)
    if not data.empty:
        df_prices[symbol] = data['Close']

# 欠損値を処理（前日データで補完）
df_prices.fillna(method='ffill', inplace=True)
df_prices.fillna(method='bfill', inplace=True)


start_prices = df_prices.iloc[0]
end_prices = df_prices.iloc[-1]
df_performance = df_prices.divide(start_prices).multiply(100)


performance = ((end_prices - start_prices) / start_prices) * 100

# パフォーマンスの表示
print("\n=== Final Performance of Stocks ===")
for symbol, name in symbols_with_names.items():
    if symbol in performance:
        # マイナス表示を明確にする
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
    # グラフ上に最終パフォーマンスを注釈として追加
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
plt.title('Japanese Stock Performance (2025)')
plt.legend(loc='upper left', fontsize=8, ncol=2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()


plt.show()

