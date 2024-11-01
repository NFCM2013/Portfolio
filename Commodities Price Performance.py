import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

commodities = ['任意', '任意', '任意', '任意', '任意',] 

start_date = ''任意'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

df_commodities = pd.DataFrame()

for commodity in commodities:
    data = yf.download(commodity, start=start_date, end=end_date)
    df_commodities[commodity] = data['Close']

start_prices = df_commodities.iloc[0]
df_performance = df_commodities.divide(start_prices).multiply(100)

plt.figure(figsize=(12, 6))

for commodity in commodities:
    plt.plot(df_performance.index, df_performance[commodity], label=commodity)

plt.xlabel('Date')
plt.ylabel('Performance (%)')
plt.title('Commodities Performance in 2024')
plt.legend()
plt.grid(True)
plt.show()