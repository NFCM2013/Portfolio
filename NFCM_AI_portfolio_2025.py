import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.dates as mdates
import japanize_matplotlib

# 銘柄コードと銘柄名の辞書
symbols_with_names = {
    '1766.T': '東建コーポレーション',
    '2175.T': 'エス・エム・エス',
    '2201.T': '森永製菓',
    '2317.T': 'システナ',
    '2353.T': '日本駐車場開発',
    '3186.T': 'ネクステージ',
    '3231.T': '野村不動産ホールディングス',
    '4966.T': '上村工業',
    '5310.T': '東洋炭素',
    '5423.T': '東京製鉄',
    '6013.T': 'タクマ',
    '6055.T': 'ジャパンマテリアル',
    '6080.T': 'M&Aキャピタルパートナーズ',
    '6088.T': 'シグマクシス・ホールディングス',
    '6101.T': 'ツガミ',
    '6200.T': 'インソース',
    '6284.T': '日精エー・エス・ビー機械',
    '6315.T': 'TOWA',
    '6420.T': 'フクシマガリレイ',
    '7164.T': '全国保証',
    '7512.T': 'イオン北海道',
    '7575.T': '日本ライフライン',
    '7818.T': 'トランザクション',
    '9247.T': 'TREホールディングス',
    '9416.T': 'ビジョン',
    '9934.T': '因幡電機産業'
}

# 期間の設定
start_date = '任意'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# 株価データの取得
df_prices = pd.DataFrame()
for symbol, name in symbols_with_names.items():
    print(f"Fetching data for {symbol} ({name})...")
    data = yf.download(symbol, start=start_date, end=end_date)
    if not data.empty:
        df_prices[symbol] = data['Close']

# 欠損値の処理
df_prices.fillna(method='ffill', inplace=True)
df_prices.fillna(method='bfill', inplace=True)

# パフォーマンスの計算
start_prices = df_prices.iloc[0]
end_prices = df_prices.iloc[-1]
df_performance = df_prices.divide(start_prices).multiply(100)
performance = ((end_prices - start_prices) / start_prices) * 100

# パフォーマンスの表示
print("\n=== Final Performance of Stocks ===")
for symbol, name in symbols_with_names.items():
    if symbol in performance:
        performance_value = performance[symbol]
        sign = "-" if performance_value < 0 else "+"
        print(f"{name} ({symbol}): {sign}{abs(performance_value):.2f}%")

# グラフの作成
plt.figure(figsize=(14, 8))
num_colors = len(symbols_with_names)
cmap = cm.get_cmap('tab20', num_colors)
colors = [cmap(i) for i in range(num_colors)]
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X']

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
    # 最終パフォーマンスの注釈
    performance_value = performance[symbol]
    sign = "-" if performance_value < 0 else "+"
    plt.text(
        df_performance.index[-1],
        df_performance[symbol].iloc[-1],
        f"{sign}{abs(performance_value):.2f}%",
        fontsize=8,
        color=color
    )

# グラフの装飾
plt.xlabel('Date')
plt.ylabel('Performance (%)')
plt.title('Japanese Stock Performance (2025)')
plt.legend(loc='upper left', fontsize=8, ncol=2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# グラフを表示
plt.show()
