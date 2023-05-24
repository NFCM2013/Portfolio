import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

df = pd.read_csv("arbitrary data")
df.head()

df.isnull().sum()

df.info()

df.columns

# data cleaning
df['Valuation ($B)'] = df['Valuation ($B)'].str.replace('$', '').astype(float)


# create a bar chart of the top 10 countries
country_counts = df['Country'].value_counts()

# select the top 10 countries based on frequency
top_countries = country_counts[:10]


top_countries.plot(kind='bar')
plt.title('Top 10 Countries with the Most Number of Startups')
plt.xlabel('Country')
plt.ylabel('Number of Startups')
plt.show()



# Distribution of Top 10 Industries
industry_counts = df['Industry'].value_counts()
top_industries = industry_counts[:10]

plt.pie(top_industries, labels=top_industries.index, autopct='%1.1f%%', startangle=90, counterclock=False)
plt.title('Distribution of Top 10 Industries')
plt.show()


# Top 15 Startups by Valuation
top_15 = df.sort_values(by='Valuation ($B)', ascending=False).head(15)

plt.figure(figsize=(12, 8))
ax = sns.barplot(x='Valuation ($B)', y='Company', data=top_15)
ax.set_ylabel('Company')
ax.set_xlabel('Valuation (US$ billions)')
ax.set_title('Top 15 Startups by Valuation')
plt.show()


