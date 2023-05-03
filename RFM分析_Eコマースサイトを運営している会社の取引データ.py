import pandas as pd
import numpy as np

online_retail = pd.read_excel("Online Retail.xlsx")
online_retail.head()

online_retail.info()


# 数値データの集計
online_retail.describe()


# 会員に限定して分析
online_retail = online_retail.loc[online_retail["CustomerID"] != "", :]
online_retail.info()


# データクレンジング
online_retail = online_retail.loc[online_retail["UnitPrice"] > 0, :]
online_retail = online_retail.loc[online_retail["Quantity"] > 0, :]


# 2011年10月末までを来店の集計期間にする
train_df = online_retail.loc[online_retail["InvoiceDate"] < "2011-11-01",]


# RFM分析
import datetime

def transform(data_df):
    days = max(data_df.loc[:, "InvoiceDate"]) - min(data_df.loc[:, "InvoiceDate"])

    # Recency
    recency = (datetime.datetime(2011, 11, 1) - data_df.groupby("CustomerID")["InvoiceDate"].max()).apply(lambda x: x.days)
    recency.name = "recency"

    # Frequency
    frequency = data_df.groupby("CustomerID")["InvoiceNo"].nunique() / days.days
    frequency.name = "frequency"

    # Monetary
    data_process_df = data_df.copy()
    data_process_df.loc[:, "total_price"] = data_process_df.loc[:, "Quantity"] * data_process_df.loc[:, "UnitPrice"]
    monetary = data_process_df.groupby("CustomerID")["total_price"].sum()
    monetary.name = "monetary"

    return pd.merge(recency, frequency, left_index=True, right_index=True).merge(monetary, left_index=True, right_index=True)

def is_visit(data_df, visitors):
    data_prcess_df = data_df.copy()
    data_prcess_df.loc[:, "is_visit"] = data_prcess_df.loc[:, "CustomerID"].apply(lambda x: x in visitors)
    return data_prcess_df.groupby("CustomerID")["is_visit"].max()

df_rfm = transform(train_df)
df_rfm



# 11月に購入実績のあるCustomerIDを取得
nov_customers = online_retail.loc[(online_retail["InvoiceDate"] >= "2011-11-01") & (online_retail["InvoiceDate"] < "2011-12-01"), "CustomerID"].unique()

# 10月末までのCustomerで11月に購入実績があるかを判定
visit_df = is_visit(train_df, nov_customers)

# RFM分析の結果と結合する
all_df = pd.merge(df_rfm, visit_df, left_index=True, right_index=True).reset_index()
all_df

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "notebook"

#
df_customer = online_retail.query("CustomerID == '14646'")[["InvoiceDate", "Quantity", "UnitPrice"]]
df_customer["Total"] = online_retail["Quantity"] * online_retail["UnitPrice"]
df_customer_sum = df_customer[["InvoiceDate", "Total"]].groupby("InvoiceDate").sum().reset_index()
fig = go.Figure(data=go.Scatter(x=df_customer_sum["InvoiceDate"], y=df_customer_sum["Total"]))
fig.show()


#
country_count_df = online_retail[["InvoiceNo", "Country"]].\
    drop_duplicates()[["Country"]].\
    value_counts().\
    reset_index(name="count")
country_count_df.loc[country_count_df['count'] < 100, 'Country'] = 'Other countries'
fig = px.pie(country_count_df, values='count', names='Country')
fig.show()


#
rfm_mean_df = all_df[["recency", "frequency", "monetary", "is_visit"]].groupby("is_visit").mean().reset_index()

col_names=['recency']
fig = go.Figure(data=[
    go.Bar(name='is_visit=False', x=col_names, y=list(rfm_mean_df.query("is_visit==False")[col_names].to_records(index=False)[0])),
    go.Bar(name='is_visit=True', x=col_names, y=list(rfm_mean_df.query("is_visit==True")[col_names].to_records(index=False)[0]))
])
fig.update_layout(barmode='group')
fig.show()


#
fig = px.histogram(all_df, x="recency")
fig.show()


#
fig = make_subplots(rows=2, cols=1)
fig.append_trace(
    go.Histogram(
        x=all_df[all_df["is_visit"] == 1]["recency"], histnorm='probability', name="翌月に来訪"
    ), 1, 1)
fig.append_trace(
    go.Histogram(
        x=all_df[all_df["is_visit"] == 0]["recency"], histnorm='probability', name="翌月に非来訪"
    ), 2, 1)
fig.show()


#
fig = px.scatter(x=all_df["recency"], y=all_df["frequency"])
fig.show()


#
fig = px.scatter(all_df, x="recency", y="frequency", size="monetary", color="is_visit", log_x=True,size_max=30)
fig.show()

