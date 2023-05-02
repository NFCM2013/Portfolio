# ニュース記事のデータをダウンロード

!wget https://www.rondhuit.com/download/ldcc-20140209.tar.gz


# 圧縮ファイルの解凍
import tarfile

with tarfile.open('ldcc-20140209.tar.gz') as tar:
    for i in tar.getmembers():
        if i.name[0] == '/' or i.name[0:2] == '..':
            exit()
    
    tar.extractall()


# 形態素解析
from janome.tokenizer import Tokenizer
import os, glob

# Janomeを使って形態素解析
ja_tokenizer = Tokenizer()


# 形態素解析
# 日本語の単語や品詞ごとに分ける
def ja_tokenize(text):
    res=[]
    lines=text.split('\n')
    # 最初の2行はヘッダーなので捨てる
    lines=lines[2:]
    for line in lines:
        malist=ja_tokenizer.tokenize(line)
        for tok in malist:
            ps=tok.part_of_speech.split(',')[0]
            # 他の品詞は無視
            if not ps in ['名詞', '動詞', '形容詞']: continue
            w=tok.base_form
            if w=='*' or w=='': w=tok.surface
            if w=='' or w=='\n': continue
            res.append(w)
        res.append('\n')
    return res


# 形態素解析
# テストデータを読み込み
root_dir = 'text'
for path in glob.glob(root_dir + '/*/*.txt', recursive=True):
    
    # LICENSE.txtは除く
    if path.find('LICENSE')>0: continue
    print(path)
    path_wakati=path + '.wakati'
    
    # ファイルができているときはスルー
    if os.path.exists(path_wakati): continue
        
    # エンコーディングに注意
    text=open(path, 'r', encoding='utf-8').read()
    
    words=ja_tokenize(text)
    wt=' '.join(words)
    open(path_wakati, 'w', encoding='utf-8').write(wt)

# データのベクトル化
# 単語辞書の定義

import os, glob, json

# パスの設定
root_dir = 'text'
dic_file = root_dir + '/word-dic.json'
data_file = root_dir + '/textdata.json'

# 単語辞書の定義
word_dic = {'_MAX':0}

# データのベクトル化
# 辞書に全ての単語を登録

def register_dic():
    files=glob.glob(root_dir+'/*/*.wakati', recursive=True)
    for i in files:
        file_to_ids(i)
        
# ファイルを読んで固定長シーケンスを返す
def file_to_ids(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        text=f.read()
        return text_to_ids(text)

# データのベクトル化
# 語句を区切ってラベリング

def text_to_ids(text):
    text=text.strip()
    words=text.split(' ')
    result=[]
    for n in words:
        n=n.strip()
        if n=='': continue
        # まだ登録していない言葉の場合    
        if not n in word_dic:
            wid=word_dic[n]=word_dic['_MAX']
            word_dic['_MAX']+=1
            print(wid, n)
        else:
            # 登録済みの言葉の場合
            wid=word_dic[n]
        result.append(wid)
    return result


# データのベクトル化
# ジャンルごとにファイルを読み込み

def count_freq(limit=0):
    X=[]
    Y=[]
    max_words = word_dic['_MAX']
    cat_names=[]
    for cat in os.listdir(root_dir):
        cat_dir = root_dir + '/' + cat
        # ファルダは無視する
        if not os.path.isdir(cat_dir):continue
        cat_idx=len(cat_names)
        cat_names.append(cat)
        files=glob.glob(cat_dir + '/*.wakati')
        i=0
        for path in files:
            # print(path)
            cnt=count_file_freq(path)
            X.append(cnt)
            Y.append(cat_idx)
            if limit > 0:
                if i > limit : break
                i += 1
    return X, Y


# データのベクトル化
# ファイル内の単語をカウント

def count_file_freq(fname):
    cnt=[0 for n in range(word_dic['_MAX'])]
    with open(fname, 'r', encoding='utf-8') as f:
        text=f.read().strip()
        ids=text_to_ids(text)
        for wid in ids:
            cnt[wid] += 1
    return cnt


# データのベクトル化
# 単語辞書の作成

if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    register_dic()
    json.dump(word_dic, open(dic_file, 'w', encoding='utf-8'))


# データのベクトル化
# 単語データのベクトル化

# ファイルごとの単語出現頻度のベクトルを作る
print('要素数=' + str(len(word_dic)))
X, Y=count_freq(100)
json.dump({'X': X, 'Y':Y}, open(data_file, 'w', encoding='utf-8'))
print('ファイル変換終了')


# 説明変数の設定
# 全ての単語ベクトルを説明変数として使用

# 1 : ライブラリのインポート
from sklearn import naive_bayes, metrics, preprocessing, model_selection
import json
import numpy

# 2 : データ準備
nb_classes=9
data=json.load(open('text/textdata.json'))
# 単語ベクトル
X=data['X']
# クラスラベル
Y=data['Y']

# 最大単語数
max_words=len(X[0])


# データの分割
# 読み込んだデータを学習用データと検証用データに分割

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=0)


# ナイーブベイズ（多項分布）の学習モデルを作成
# 3 : 機械学習で分類・識別する
clf = naive_bayes.MultinomialNB(alpha=0.1, fit_prior='True')


# K分割交差検証
# K分割交差検証法を用いて学習モデルを評価（K=10)

scores=model_selection.cross_val_score(clf, X, Y, cv=10)

print('平均正解率 = ', scores.mean())
print('正解率の標準偏差 = ', scores.std())

