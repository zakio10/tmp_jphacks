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

#データ参照用jsonファイル読み込み
with open('data/ref_data.json', mode='r') as f:
    ref_data = json.load(f)

en_data = data['en']
ja_data = data['ja']
en_data_keys = en_data.keys()
ja_data_keys = ja_data.keys()

print('english data len :',len(en_data))
print('japanese data len :',len(ja_data))


#Doc2vecモデル読み込み
en_doc2vec_model = Doc2Vec.load('model/en_doc2vec.model')
ja_doc2vec_model = Doc2Vec.load('model/ja_doc2vec.model')


#Word2vecモデル読み込み
en_word2vec_model = KeyedVectors.load_word2vec_format('model/en_word2vec.bin', binary=True)
ja_word2vec_model = KeyedVectors.load_word2vec_format('model/ja_word2vec.bin', binary=True)


#テスト
test_class_ids = ['11610212', '30562111', '51100303']
check_list = ['major', 'name', 'summary', 'url']


for test_class_id in test_class_ids:
    print("================================================================")
    print('class_id :', test_class_id)
    for tmp_check in check_list:
        print(tmp_check, ' :', ref_data[test_class_id][tmp_check])
    print("================================================================")
    #類似講義
    wmd_list = []
    info_list = []
    similar_class_id_list = []


    tmp_similar_list = ja_doc2vec_model.docvecs.most_similar(test_class_id, topn=100) #類似講義上位500件
    for similar_class in tmp_similar_list:
        similar_class_id = similar_class[0]
        tmp_wmd = ja_word2vec_model.wmdistance(ja_data[test_class_id].split(' '), ja_data[similar_class_id].split(' '))
        wmd_list.append(tmp_wmd)
        similar_class_id_list.append(similar_class_id)
        tmp_check_list = []
        for tmp_check in check_list:
            tmp_check_list.append(''.join([tmp_check, ' :', ref_data[similar_class_id][tmp_check]]))
        info_list.append(tmp_check_list)

    #wmd上位10件
    wmd_list = np.array(wmd_list)
    argsort_wmd = np.argsort(wmd_list)[:10]

    for index in list(argsort_wmd):
        print('class_id :', similar_class_id_list[index], 'wmd_score :', wmd_list[index])
        infos = info_list[index]
        for info in infos:
            print(info)
        print('----------------------------------------------------------------')
    
    print('\n')

# for test_class_id in test_class_ids:
#     print("================================================================")
#     print('class_id :', test_class_id)
#     for tmp_check in check_list:
#         print(tmp_check, ' :', ref_data[test_class_id][tmp_check])
#     print('----------------------------------------------------------------')
#     #類似講義
#     tmp_similar_list = ja_doc2vec_model.docvecs.most_similar(test_class_id)[:10]
#     for similar_class in tmp_similar_list:
#         similar_class_id = similar_class[0]
#         similar_class_level = similar_class[1]
#         print('class_id :', similar_class_id, 'similar_level :', similar_class_level)
#         for tmp_check in check_list:
#             print(tmp_check, ' :', ref_data[similar_class_id][tmp_check])
#         print('----------------------------------------------------------------')
    
#     print('\n')