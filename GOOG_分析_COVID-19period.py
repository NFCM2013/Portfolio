! pip install yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import yfinance as yf
from datetime import date, timedelta

today = date.today()
today

end_date = today.strftime("%Y-%m-%d")
end_date

d1 = date.today() - timedelta(days=360*5)
d1

start_date = d1.strftime("%Y-%m-%d")
start_date

# 5年間のデータを取得
data = yf.download(tickers = "GOOGL",
                  start = start_date,
                  end = end_date)
data.shape

data.head()

# データクレンジング
data.reset_index(inplace=True)
data

# グラフで可視化
plt.figure(figsize=(12,4))
sns.set_style("ticks")
sns.lineplot(data=data,x="Date",y="High",color="firebrick")

# COVID-19の最初の症例は、2019年12月に中国の武漢で報告
plt.axvspan(xmin=pd.to_datetime('2019-12-1'),xmax=pd.to_datetime('2022-3-1'),color='dimgray',
            alpha=0.25)
plt.text(x=pd.to_datetime("2019-12-1"),y=data["High"].max(),size="small",
         s="*highlighted area shows the COVID-19 period")

# 日本で最初のCOVID-19の症例は、2020年1月15日
plt.vlines(x=pd.to_datetime("2020-1-15"),color="blue",ymin=data["High"].min(),
           ymax=data["High"].max()-5)
plt.annotate(text="The day first COVID-19 case reported in Japan",
             xy=(pd.to_datetime("2020-1-15"),data["High"].mean()),
             xytext=(pd.to_datetime("2018-1-1"),90),size="small",
             arrowprops=dict(facecolor="black",shrink=0.05))

# アメリカで最初のCOVID-19の症例は、2020年1月30日
plt.vlines(x=pd.to_datetime("2020-1-30"),color="red",ymin=data["High"].min(),
           ymax=data["High"].max()-5)
plt.annotate(text="The day first COVID-19 case reported in the US",
             xy=(pd.to_datetime("2020-1-30"),data["High"].mean()),
             xytext=(pd.to_datetime("2018-1-1"),100),size="small",
             arrowprops=dict(facecolor="black",shrink=0.05))

plt.title("Google Stock Prices From {0} to {1}".format(start_date,end_date),c="blue",
         alpha=0.8,size="x-large");
sns.despine()
plt.ylabel("Stock Price")