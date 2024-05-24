
    ticker_past_capitaladequacyratio = result_past_stockholdersequity['StockholdersEquity'] / result_past_totalassets['TotalAssets']

    ticker_past_roe = result_past_netincome['NetIncome'] / result_past_stockholdersequity['StockholdersEquity']

    df_financial_info = pd.DataFrame({'asOfDate':               result_past_totalrevenue['asOfDate'],
                                      'TotalRevenue':           result_past_totalrevenue['TotalRevenue'],
                                      'StockholdersEquity':     result_past_stockholdersequity['StockholdersEquity'],
                                      'TotalAssets':            result_past_totalassets['TotalAssets'],
                                      'capitalAdequacyRatio':   ticker_past_capitaladequacyratio,
                                      'ROE':                    ticker_past_roe})