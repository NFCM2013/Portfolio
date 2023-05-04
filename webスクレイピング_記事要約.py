import requests
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# 要約を生成する記事のURLを指定
url = "要約を生成する記事のURL"

# Webサイトからテキストを取得
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
paragraphs = soup.find_all("p")
text = " ".join([p.get_text() for p in paragraphs])

# LexRankアルゴリズムを使用して要約を生成
parser = HtmlParser.from_url(url, Tokenizer("japanese"))
summarizer = LexRankSummarizer()
summary_sentences = summarizer(parser.document, sentences_count=3)

# 要約を出力
print("要約：")
for sentence in summary_sentences:
    print(sentence)