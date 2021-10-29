import json
import glob
# import MeCab
import re
import tqdm
import nltk as en_tokenizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.models import KeyedVectors
import numpy as np


#学習用jsonファイル読み込み
with open('data/div_corpus_data.json', mode='r') as f:
    data = json.load(f)

# #データ参照用jsonファイル読み込み
# with open('data/ref_data.json', mode='r') as f:
#     ref_data = json.load(f)

en_data = data['en']
ja_data = data['ja']
en_data_keys = en_data.keys()
ja_data_keys = ja_data.keys()

print('english data len :',len(en_data))
print('japanese data len :',len(ja_data))


#Doc2vecモデル読み込み
en_doc2vec_model = Doc2Vec.load('model/en_doc2vec.model')
ja_doc2vec_model = Doc2Vec.load('model/ja_doc2vec.model')


# #Word2vecモデル読み込み
# en_word2vec_model = KeyedVectors.load_word2vec_format('model/en_word2vec.bin', binary=True)
# ja_word2vec_model = KeyedVectors.load_word2vec_format('model/ja_word2vec.bin', binary=True)


#テスト
test_class_ids = ['11610212', '30562111', '51100303']
check_list = ['major', 'name', 'summary', 'url']


#出力ファイル
output_data = []

#日本語講義推薦データ作成
print("日本語講義計算中...")
for ja_class_id in tqdm.tqdm(ja_data_keys):
    #一時保存用
    tmp_class_data = dict()
    tmp_similarClasses_list = []
    tmp_similarlevel_list = []

    
    tmp_class_data['code'] = ja_class_id

    #類似講義検索
    tmp_similar_list = ja_doc2vec_model.docvecs.most_similar(ja_class_id)
    for similar_class in tmp_similar_list:
        #一時保存用
        tmp_similar_class_data = dict()
        similar_class_id = similar_class[0]
        similar_class_level = similar_class[1]
        tmp_similar_class_data['code'] = similar_class_id
        tmp_similar_class_data['year'] = '2021'
        tmp_similarClasses_list.append(tmp_similar_class_data)
        tmp_similarlevel_list.append(similar_class_level)
    
    tmp_class_data['similarClasses'] = tmp_similarClasses_list
    tmp_class_data['similarLevel'] = tmp_similarlevel_list

    output_data.append(tmp_class_data)
print("日本語講義計算終了")


#英語講義推薦データ作成
print("英語講義計算中...")
for en_class_id in tqdm.tqdm(en_data_keys):
    #一時保存用
    tmp_class_data = dict()
    tmp_similarClasses_list = []
    tmp_similarlevel_list = []

    
    tmp_class_data['code'] = en_class_id

    #類似講義検索
    tmp_similar_list = en_doc2vec_model.docvecs.most_similar(en_class_id)
    for similar_class in tmp_similar_list:
        #一時保存用
        tmp_similar_class_data = dict()
        similar_class_id = similar_class[0]
        similar_class_level = similar_class[1]
        tmp_similar_class_data['code'] = similar_class_id
        tmp_similar_class_data['year'] = '2021'
        tmp_similarClasses_list.append(tmp_similar_class_data)
        tmp_similarlevel_list.append(similar_class_level)
    
    tmp_class_data['similarClasses'] = tmp_similarClasses_list
    tmp_class_data['similarLevel'] = tmp_similarlevel_list

    output_data.append(tmp_class_data)
print("英語講義計算終了")

with open('data/recommend_doc2vec.json', 'w') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)
print("データ出力")