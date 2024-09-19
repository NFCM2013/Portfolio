def get_company_metrics(ticker_num, ticker_data):
    company_metrics = [ticker_num]
    summary_detail_keys = ['dividendRate', 'dividendYield', 'fiveYearAvgDividendYield', 'payoutRatio', 'marketCap']
    for summary_detail_key in summary_detail_keys:
        try:
            company_metrics.append(ticker_data.summary_detail[ticker_num][summary_detail_key])
        except Exception:
            company_metrics.append(np.nan)

    financial_data_keys = ['totalRevenue', 'returnOnEquity']
    for financial_data_key in financial_data_keys:
        try:
            company_metrics.append(ticker_data.financial_data[ticker_num][financial_data_key])
        except Exception:
            company_metrics.append(np.nan)

    columns = ['ticker', 'dividendRate', 'dividendYield', 'fiveYearAvgDividendYield', 'payoutRatio', 'MarketCap', 'totalRevenue', 'ROE']
    df_company_metrics = pd.DataFrame(data=[company_metrics], columns=columns)

    return df_company_metrics