import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.dates as mdates
import japanize_matplotlib
from tqdm import tqdm
import time


symbols_with_names = {
    '1766.T': '東建コーポレーション',
    '2175.T': 'エス・エム・エス',
    '2201.T': '森永製菓',
    '2317.T': 'システナ',
    '2353.T': '日本駐車場開発',
    '3186.T': 'ネクステージ',
    '3231.T': '野村不動産ホールディングス',
    '4373.T': 'シンプレクス・ホールディングス',
    '4966.T': '上村工業',
    '5310.T': '東洋炭素',
    '5423.T': '東京製鐵',
    '6013.T': 'タクマ',
    '6055.T': 'ジャパンマテリアル',
    '6080.T': 'Ｍ＆Ａキャピタルパートナーズ',
    '6088.T': 'シグマクシス・ホールディングス',
    '6101.T': 'ツガミ',
    '6196.T': 'ストライク',
    '6200.T': 'インソース',
    '6284.T': '日精エー・エス・ビー機械',
    '6420.T': 'フクシマガリレイ',
    '6914.T': 'オプテックスグループ',
    '7575.T': '日本ライフライン',
    '7818.T': 'トランザクション',
    '7972.T': 'イトーキ',
    '9247.T': 'ＴＲＥホールディングス',
    '9416.T': 'ビジョン',
    '9621.T': '建設技術研究所',
    '9824.T': '泉州電業',
    '9928.T': 'ミロク情報サービス'
}

# 期間設定
start_date = '任意'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# 株価データ取得
df_prices = pd.DataFrame()

print("データ取得中...")
for symbol, name in tqdm(symbols_with_names.items()):
    for attempt in range(3): 
        try:
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            if not data.empty:
                df_prices[symbol] = data['Close']
            break
        except Exception as e:
            print(f"{symbol} の取得に失敗しました (試行{attempt + 1}/3): {e}")
            time.sleep(2)

# 欠損値処理
df_prices.dropna(axis=1, how='all', inplace=True)  
df_prices.fillna(method='ffill', inplace=True)
df_prices.fillna(method='bfill', inplace=True)

# パフォーマンス計算
start_prices = df_prices.iloc[0]
end_prices = df_prices.iloc[-1]
df_performance = df_prices.divide(start_prices).multiply(100)
performance = ((end_prices - start_prices) / start_prices) * 100

# パフォーマンス出力
print("\n=== 銘柄別パフォーマンス ===")
for symbol, name in symbols_with_names.items():
    if symbol in performance:
        value = performance[symbol]
        sign = "+" if value >= 0 else "-"
        print(f"{name} ({symbol}): {sign}{abs(value):.2f}%")

# グラフ描画
plt.figure(figsize=(14, 8))
num_colors = len(df_performance.columns)
cmap = cm.get_cmap('tab20', num_colors)
colors = [cmap(i) for i in range(num_colors)]
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X']

for i, symbol in enumerate(df_performance.columns):
    name = symbols_with_names[symbol]
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
        markersize=5
    )
    plt.text(
        df_performance.index[-1],
        df_performance[symbol].iloc[-1],
        f"{performance[symbol]:+.1f}%",
        fontsize=8,
        color=color
    )

plt.xlabel('日付')
plt.ylabel('パフォーマンス (%)')
plt.title('パフォーマンス')
plt.legend(loc='upper left', fontsize=8, ncol=2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
