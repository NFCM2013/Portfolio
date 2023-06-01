import tweepy
import re
from collections import Counter

# Twitter APIの認証情報を設定
consumer_key = "Your Consumer Key"
consumer_secret = "Your Consumer Secret"
access_token = "Your Access Token"
access_token_secret = "Your Access Token Secret"

# 認証情報を使ってAPIクライアントを作成
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def analyze_hashtags(keyword, num_tweets):
    # キーワードを含むツイートを収集
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang='en', tweet_mode='extended').items(num_tweets)

    hashtags = []
    for tweet in tweets:
        # ツイートの本文からハッシュタグを抽出
        hashtags += re.findall(r"#(\w+)", tweet.full_text)

    # ハッシュタグの出現頻度を解析
    hashtag_freq = Counter(hashtags)
    top_hashtags = hashtag_freq.most_common(10)  # 上位10件のハッシュタグを取得

    return top_hashtags

keyword = "Python"  # 検索するキーワード
num_tweets = 1000  # 収集するツイートの数

top_hashtags = analyze_hashtags(keyword, num_tweets)

# 結果を表示
for hashtag, count in top_hashtags:
    print(f"{hashtag}: {count}回")

