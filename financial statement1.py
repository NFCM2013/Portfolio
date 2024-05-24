
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
