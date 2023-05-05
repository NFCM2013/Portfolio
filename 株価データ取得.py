import pandas as pd
import yfinance as yf
import time

def get_stock_data(symbol, start_date, end_date):
    # データ格納用のリストを作成
    data_list = []
    # 1年単位でデータを取得する
    for year in range(start_date.year, end_date.year+1):
        # データ取得用の期間を設定
        from_date = pd.Timestamp(year, 1, 1)
        to_date = pd.Timestamp(year, 12, 31)
        # Yahoo Finance APIを使用して株価データを取得
        retry_count = 0
        while retry_count < 3:
            try:
                stock_data = yf.download(symbol, start=from_date, end=to_date)
                break
            except Exception as e:
                print(f"Error occurred during downloading stock data: {e}")
                print(f"Retrying after 3 seconds...")
                retry_count += 1
                time.sleep(3)
        else:
            print("Max retries exceeded. Skipping this year.")
            continue
        # データをリストに追加
        data_list.append(stock_data)
    # リストに格納されたデータを結合してデータフレームに変換
    symbol_data = pd.concat(data_list)
    # データフレームを返す
    return symbol_data

# 取得対象の期間を設定
start_date = pd.Timestamp('2000-01-01')
end_date = pd.Timestamp.now()

# S&P 500の株価データを取得
symbol_data = get_stock_data('^GSPC', start_date, end_date)

# csvファイルに保存する
symbol_data.to_csv('SP500_stock_data.csv')