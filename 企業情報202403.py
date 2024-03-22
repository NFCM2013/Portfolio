import os
import numpy as np
import pandas as pd
from yahooquery import Ticker
from tqdm import tqdm

def main():
    is_file = os.path.isfile('jp.xls')
    if is_file:
        print('東証上場銘柄')
        df_data_j = pd.read_excel('jp.xls', index_col=None)
    else:
        print('保存')
        exit()

    df_data_j = df_data_j[df_data_j['市場・商品区分'] != 'REIT・ベンチャーファンド・カントリーファンド・インフラファンド']

    df_data_j = df_data_j[df_data_j['市場・商品区分'] != 'ETF・ETN']

    df_data_j = df_data_j[df_data_j['コード'] != 25935]

    df_company_metrics = pd.DataFrame()
    df_company_financial_info = pd.DataFrame()

    series_ticker_name = pd.Series()
    series_market_product_category = pd.Series()
    series_type_33 = pd.Series()
    series_type_17 = pd.Series()

    
    for ticker in tqdm(df_data_j['コード']):
        
        df_data_j_filter = df_data_j[df_data_j['コード'] == ticker]
        ticker_num = str(ticker) + '.T'
        ticker_data = Ticker(ticker_num)

        series_ticker_name = pd.concat([series_ticker_name, df_data_j_filter['銘柄名']])
        series_market_product_category = pd.concat([series_market_product_category, df_data_j_filter['市場・商品区分']])
        series_type_33 = pd.concat([series_type_33, df_data_j_filter['33業種区分']])
        series_type_17 = pd.concat([series_type_17, df_data_j_filter['17業種区分']])

        # 企業情報の指標、財務状況を取得する
        df_company_metrics = pd.concat([df_company_metrics, get_company_metrics(ticker_num, ticker_data)])
        df_company_financial_info = pd.concat([df_company_financial_info, get_company_finacial_info(ticker_data)])

    # 銘柄名を追加し、列を並び替える
    df_company_metrics['ticker_name'] = series_ticker_name.values
    df_company_metrics['market_product_category'] = series_market_product_category.values
    df_company_metrics['type_33'] = series_type_33.values
    df_company_metrics['type_17'] = series_type_17.values
    columns = ['ticker', 'ticker_name', 'market_product_category',
               'type_33', 'type_17', 'dividendRate', 'dividendYield',
               'fiveYearAvgDividendYield', 'payoutRatio', 'MarketCap',
               'totalRevenue', 'ROE']
    df_company_metrics = df_company_metrics.reindex(columns=columns)

    
    df_company_metrics.to_csv('company_metrics.csv', encoding='cp932', index=False, errors='ignore')
    df_company_financial_info.to_csv('company_financial_info.csv', encoding='cp932', index=False, errors='ignore')


def get_company_metrics(ticker_num, ticker_data):
    
    company_metrics = [ticker_num]

    
    summary_detail_keys = ['dividendRate', 'dividendYield', 'fiveYearAvgDividendYield', 'payoutRatio', 'marketCap']
    for summary_detail_key in summary_detail_keys:
        try:
            company_metrics.append(ticker_data.summary_detail[ticker_num][summary_detail_key])
        except Exception as e:
            print('証券コード:{},未取得の属性:{}'.format(ticker_num, summary_detail_key))
            company_metrics.append(np.nan)

    
    financial_data_keys = ['totalRevenue', 'returnOnEquity']
    for financial_data_key in financial_data_keys:
        try:
            company_metrics.append(ticker_data.financial_data[ticker_num][financial_data_key])
        except Exception as e:
            print('証券コード:{},未取得の属性:{}'.format(ticker_num, financial_data_key))
            company_metrics.append(np.nan)

    
    columns = ['ticker', 'dividendRate', 'dividendYield', 'fiveYearAvgDividendYield',
               'payoutRatio', 'MarketCap', 'totalRevenue', 'ROE']
    df_company_metrics = pd.DataFrame(data=[company_metrics], columns=columns)

    return df_company_metrics



def get_company_finacial_info(ticker_data):
    # income_statement(損益計算書)、cash_flow、balance_sheet(貸借対照表)を取得する
    try:
        income_statement = ticker_data.income_statement(trailing=False)
        cash_flow = ticker_data.cash_flow(trailing=False)
        balance_sheet = ticker_data.balance_sheet()
    except Exception as e:
        print(e)
        return

    # 過去の売上高、純利益、純資産、総資産を取得する
    try:
        past_totalrevenue = income_statement[['asOfDate', 'TotalRevenue']]
        past_netincome = cash_flow[['asOfDate', 'NetIncome']]
        past_stockholdersequity = balance_sheet[['asOfDate', 'StockholdersEquity']]
        past_totalassets = balance_sheet[['asOfDate', 'TotalAssets']]
    except Exception as e:
        print(e)
        return

    # income_statement(損益計算書)、cash_flow、balance_sheet(貸借対照表)の決算日を取得する
    past_totalrevenue_asofdate = income_statement['asOfDate']
    past_netincome_asofdate = cash_flow['asOfDate']
    past_stockholdersequity_asofdate = balance_sheet['asOfDate']
    past_totalassets_asofdate = balance_sheet['asOfDate']

    # 損益計算書、キャッシュフロー、貸借対照表で取得できる決算日が異なる場合
    # 損益計算書、キャッシュフロー、貸借対照表の決算日が共通の日時を抽出する
    common_asofdate = set(past_totalassets_asofdate).intersection(set(past_netincome_asofdate)).intersection(set(past_stockholdersequity_asofdate)).intersection(set(past_totalrevenue_asofdate))

    # 共通している日時の売上高、純利益、純資産、総資産を抽出する
    result_past_totalrevenue = pd.DataFrame()
    result_past_netincome = pd.DataFrame()
    result_past_stockholdersequity = pd.DataFrame()
    result_past_totalassets = pd.DataFrame()

    for asofdate in common_asofdate:
        result_past_totalrevenue = pd.concat([result_past_totalrevenue, past_totalrevenue[past_totalrevenue['asOfDate'] == asofdate]])
        result_past_netincome = pd.concat([result_past_netincome, past_netincome[past_netincome['asOfDate'] == asofdate]])
        result_past_stockholdersequity = pd.concat([result_past_stockholdersequity, past_stockholdersequity[past_stockholdersequity['asOfDate'] == asofdate]])
        result_past_totalassets = pd.concat([result_past_totalassets, past_totalassets[past_totalassets['asOfDate'] == asofdate]])

    # 時刻で昇順に並び替える
    result_past_totalrevenue = result_past_totalrevenue.sort_values('asOfDate')
    result_past_netincome = result_past_netincome.sort_values('asOfDate')
    result_past_stockholdersequity = result_past_stockholdersequity.sort_values('asOfDate')
    result_past_totalassets = result_past_totalassets.sort_values('asOfDate')

    # 過去の自己資本比率を計算する
    ticker_past_capitaladequacyratio = result_past_stockholdersequity['StockholdersEquity'] / result_past_totalassets['TotalAssets']

    # 過去の自己資本利益率を計算する
    ticker_past_roe = result_past_netincome['NetIncome'] / result_past_stockholdersequity['StockholdersEquity']

    # 企業情報の過去の指標を保存する
    # 過去の売上高,純利益,総資産,自己資本比率,自己資本利益率
    df_financial_info = pd.DataFrame({'asOfDate':               result_past_totalrevenue['asOfDate'],
                                      'TotalRevenue':           result_past_totalrevenue['TotalRevenue'],
                                      'StockholdersEquity':     result_past_stockholdersequity['StockholdersEquity'],
                                      'TotalAssets':            result_past_totalassets['TotalAssets'],
                                      'capitalAdequacyRatio':   ticker_past_capitaladequacyratio,
                                      'ROE':                    ticker_past_roe})

    df_financial_info = df_financial_info.reset_index()

    return df_financial_info


if __name__ == "__main__":
    main()
