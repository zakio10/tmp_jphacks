import json
from gensim.models.doc2vec import Doc2Vec
from gensim.models import KeyedVectors
import numpy as np


#クエリID
query_id = '11610212' #ここに検索する対象の講義のIDを入れて

#返り値
wmd_list = [] #WMDスコア
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
    #Word2vecモデル読み込み
    en_word2vec_model = KeyedVectors.load_word2vec_format('model/en_word2vec.bin', binary=True)
    
    tmp_similar_list = en_doc2vec_model.docvecs.most_similar(query_id, topn=100) #類似講義上位100件
    for similar_class in tmp_similar_list:
        similar_class_id = similar_class[0]
        tmp_wmd = en_word2vec_model.wmdistance(ja_data[query_id].split(' '), ja_data[similar_class_id].split(' '))
        wmd_list.append(tmp_wmd)
        similar_class_id_list.append(similar_class_id)

    #wmd上位10件
    wmd_list = list(np.array(wmd_list))
    argsort_wmd = list(np.argsort(wmd_list)[:10])
    similar_class_id_list = [similar_class_id_list[index] for index in argsort_wmd] #類似講義上位10件(0番目から順に最も類似している)
    wmd_list = [wmd_list[index] for index in argsort_wmd] #類似講義上位10件の類似度(0が最も類似している)
elif query_id in ja_data_keys:
    #日本語講義
    #Doc2vecモデル読み込み
    ja_doc2vec_model = Doc2Vec.load('model/en_doc2vec.model')
    #Word2vecモデル読み込み
    ja_word2vec_model = KeyedVectors.load_word2vec_format('model/ja_word2vec.bin', binary=True)

    tmp_similar_list = ja_doc2vec_model.docvecs.most_similar(query_id, topn=100) #類似講義上位100件
    for similar_class in tmp_similar_list:
        similar_class_id = similar_class[0]
        tmp_wmd = ja_word2vec_model.wmdistance(ja_data[query_id].split(' '), ja_data[similar_class_id].split(' '))
        wmd_list.append(tmp_wmd)
        similar_class_id_list.append(similar_class_id)

    #wmd上位10件
    wmd_list = list(np.array(wmd_list))
    argsort_wmd = list(np.argsort(wmd_list)[:10])
    similar_class_id_list = [similar_class_id_list[index] for index in argsort_wmd] #類似講義上位10件(0番目から順に最も類似している)
    wmd_list = [wmd_list[index] for index in argsort_wmd] #類似講義上位10件の類似度(0が最も類似している)
else:
    #エラー該当講義なし
    pass

# 確認用
# print(similar_class_id_list)
# print(wmd_list)

#返り値
# similar_class_id_list : 類似講義上位10件の講義ID(0番目から順に最も類似している)
# wmd_list : 類似講義上位10件の類似度(0が最も類似している)