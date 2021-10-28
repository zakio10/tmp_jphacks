# シラバスコーパス作成ツール
シラバスのjsonファイルからデータを前処理してコーパスデータを作成する．  
前処理は＜概要/Course Content Summary＞ + ＜到達目標/Goals,Aims＞ + ＜授業計画/Schedule＞の（内容/Contents）を取り出し連結する．英語のみのデータは英語形態素解析器(nltk)によって分かち書き，日本語が含まれるデータはMeCabで分かち書き．数字，教員名，記号を削除．  
作成されるjsonデータは講義IDに対して，前処理された講義の「＜概要/Course Content Summary＞ + ＜到達目標/Goals,Aims＞ + ＜授業計画/Schedule＞の（内容/Contents）を取り出し連結」したものが対になっている．

## 環境
[packages]
gensim = "*"
mecab-python3 = "*"
tqdm = "*"
nltk = "*"

MeCabの辞書はmecab-ipadic-NEologd
https://github.com/neologd/mecab-ipadic-neologd

## 使い方
「2021.json」をダウンロードして，フォルダに配置する．(./data/2021.json)


英語用形態素解析器の準備(ターミナルなどで事前準備)(3.3G)
```
$python
>>import nltk
>>nltk.download('all')
```
おもすぎる場合はこちらでも良い．
```
$python
>>import nltk
>>nltk.download('punkt')
>>nltk.download('averaged_perceptron_tagger')
```

コーパスデータ作成
```
python make_data.py
```
![サンプル](https://github.com/zakio10/tmp_jphacks/blob/master/app.jpg)

モデル学習
```
python pre_train.py
```

テスト(Doc2vecバージョン)
```
python test.py
```

実際に使うのは次の2つのうちの1つ．どっちか良いモデルを使ってください．
- request_doc2vec.py
- request_wmd.py