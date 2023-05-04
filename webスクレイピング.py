import requests
from bs4 import BeautifulSoup

# スクレイピング対象のURLを指定
url = 'https://www.google.com/'

# URLからHTMLを取得する
response = requests.get(url)
html = response.text

# BeautifulSoupを使用してHTMLを解析する
soup = BeautifulSoup(html, 'html.parser')

# 特定の要素を抽出する例
title = soup.title.text  # ページのタイトルを取得する
links = soup.find_all('a')  # すべてのリンクを取得する

# 抽出したデータを出力する
print(title)
for link in links:
    print(link.get('href'))