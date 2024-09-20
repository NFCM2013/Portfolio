past_totalrevenue_asofdate = past_totalrevenue['asOfDate']
    past_netincome_asofdate = past_netincome['asOfDate']
    past_stockholdersequity_asofdate = past_stockholdersequity['asOfDate']
    past_totalassets_asofdate = past_totalassets['asOfDate']

    common_asofdate = set(past_totalassets_asofdate).intersection(set(past_netincome_asofdate)).intersection(set(past_stockholdersequity_asofdate)).intersection(set(past_totalrevenue_asofdate))

    result_past_totalrevenue = pd.DataFrame()
    result_past_netincome = pd.DataFrame()
    result_past_stockholdersequity = pd.DataFrame()
    result_past_totalassets = pd.DataFrame()

    for asofdate in common_asofdate:
        result_past_totalrevenue = pd.concat([result_past_totalrevenue, past_totalrevenue[past_totalrevenue['asOfDate'] == asofdate]])
        result_past_netincome = pd.concat([result_past_netincome, past_netincome[past_netincome['asOfDate'] == asofdate]])
        result_past_stockholdersequity = pd.concat([result_past_stockholdersequity, past_stockholdersequity[past_stockholdersequity['asOfDate'] == asofdate]])
        result_past_totalassets = pd.concat([result_past_totalassets, past_totalassets[past_totalassets['asOfDate'] == asofdate]])

    result_past_totalrevenue = result_past_totalrevenue.sort_values('asOfDate').reset_index(drop=True)
    result_past_netincome = result_past_netincome.sort_values('asOfDate').reset_index(drop=True)
    result_past_stockholdersequity = result_past_stockholdersequity.sort_values('asOfDate').reset_index(drop=True)
    result_past_totalassets = result_past_totalassets.sort_values('asOfDate').reset_index(drop=True)

    ticker_past_capitaladequacyratio = result_past_stockholdersequity['StockholdersEquity'] / result_past_totalassets['TotalAssets']
    ticker_past_roe = result_past_netincome['NetIncome'] / result_past_stockholdersequity['StockholdersEquity']

    df_financial_info = pd.DataFrame({'asOfDate': result_past_totalrevenue['asOfDate'],
                                      'TotalRevenue': result_past_totalrevenue['TotalRevenue'],
                                      'StockholdersEquity': result_past_stockholdersequity['StockholdersEquity'],
                                      'TotalAssets': result_past_totalassets['TotalAssets'],
                                      'capitalAdequacyRatio': ticker_past_capitaladequacyratio,
                                      'ROE': ticker_past_roe})