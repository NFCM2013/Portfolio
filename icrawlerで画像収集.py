from icrawler.builtin import GoogleImageCrawler

# 保存先フォルダーの指定
save_dir = './images/'

# GoogleImageCrawlerのインスタンスを生成
google_crawler = GoogleImageCrawler(storage={'root_dir': save_dir})

# 収集条件を指定
google_crawler.crawl(keyword='cat', max_num=100)