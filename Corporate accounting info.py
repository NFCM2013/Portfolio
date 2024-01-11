from google.colab import drive
drive.mount('/content/drive')  # Googleドライブをマウント
from yahooquery import Ticker
from yahooquery import Screener
import pandas as pd

# 任意の銘柄シンボルを指定して、Tickerオブジェクトを作成する
ticker_num = '任意の銘柄'
ticker_data = Ticker(ticker_num)

# Googleドライブのパス
drive_path = '/content/drive/MyDrive/任意のフォルダ/'

# 貸借対照表を取得してGoogleドライブに保存
ticker_balance_sheet = ticker_data.balance_sheet()
ticker_balance_sheet.to_csv(drive_path + 'balance_sheet.csv')

# キャッシュ・フローを取得してGoogleドライブに保存
ticker_cash_flow = ticker_data.cash_flow()
ticker_cash_flow.to_csv(drive_path + 'cash_flow.csv')

# 損益計算書を取得してGoogleドライブに保存
ticker_income_statement = ticker_data.income_statement()
ticker_income_statement.to_csv(drive_path + 'income_statement.csv')

# 評価指標を取得してGoogleドライブに保存
ticker_valuation_measures = ticker_data.valuation_measures
ticker_valuation_measures.to_csv(drive_path + 'valuation_measures.csv')

# 財務情報を取得してGoogleドライブに保存
ticker_financial_data = ticker_data.financial_data
df_Series_ticker_financial_data = {}
for k, v in ticker_financial_data.items():
    df_Series_ticker_financial_data[k] = pd.Series(v)

df_ticker_financial_data = pd.DataFrame(df_Series_ticker_financial_data)
df_ticker_financial_data.T.to_csv(drive_path + 'financial_data.csv')

# 条件を満たす銘柄を抽出してGoogleドライブに保存
s = Screener()
s_get_screeners = s.get_screeners(['most_actives', 'day_gainers'], 5)
df_Series_s_get_screeners = {}
for k, v in s_get_screeners.items():
    df_Series_s_get_screeners[k] = pd.Series(v)

df_s_get_screeners = pd.DataFrame(df_Series_s_get_screeners)
df_s_get_screeners.T.to_csv(drive_path + 'screeners.csv')
