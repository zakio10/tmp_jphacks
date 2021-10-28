import json
from gensim.models.doc2vec import Doc2Vec
import numpy as np


#クエリID
query_id = '11610212' #ここに検索する対象の講義のIDを入れて

#返り値
score_list = [] #類似スコア
similar_class_id_list = [] #類似講義

#WMD用のデータjsonファイル読み込み
with open('data/div_corpus_data.json', mode='r') as f:
    data = json.load(f)

en_data = data['en']
ja_data = data['ja']
en_data_keys = en_data.keys()
ja_data_keys = ja_data.keys()

#日本語講義か英語講義かチェック
if query_id in en_data_keys:
    #英語講義
    #Doc2vecモデル読み込み
    en_doc2vec_model = Doc2Vec.load('model/en_doc2vec.model')
    
    tmp_similar_list = en_doc2vec_model.docvecs.most_similar(query_id, topn=10) #類似講義上位100件
    for similar_class in tmp_similar_list:
        similar_class_id = similar_class[0]
        score = similar_class[1]
        similar_class_id_list.append(similar_class_id)
        score_list.append(score)

elif query_id in ja_data_keys:
    #日本語講義
    #Doc2vecモデル読み込み
    ja_doc2vec_model = Doc2Vec.load('model/ja_doc2vec.model')

    tmp_similar_list = ja_doc2vec_model.docvecs.most_similar(query_id, topn=10) #類似講義上位100件
    for similar_class in tmp_similar_list:
        similar_class_id = similar_class[0]
        score = similar_class[1]
        similar_class_id_list.append(similar_class_id)
        score_list.append(score)

else:
    #エラー該当講義なし
    pass

# 確認用
print(similar_class_id_list)
print(score_list)

#返り値
# similar_class_id_list : 類似講義上位10件の講義ID(0番目から順に最も類似している)
# score_list : 類似講義上位10件の類似度(1が最も良い(たぶん))