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

#学習データ
data = dict()
en_data = dict()
ja_data = dict()
ref_data = dict()

#doc2vec用学習データ
en_train_docs = []
ja_train_docs = []

#Word2vec学習用データ
en_train_list = []
ja_train_list = []

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

#英語講義
for tmp_key in en_data_keys:
    en_train_docs.append(TaggedDocument(words=en_data[tmp_key].split(' '), tags=[tmp_key]))
    en_train_list.append(en_data[tmp_key].split(' '))

#日本語講義
for tmp_key in ja_data_keys:
    ja_train_docs.append(TaggedDocument(words=ja_data[tmp_key].split(' '), tags=[tmp_key]))
    ja_train_list.append(ja_data[tmp_key].split(' '))

#Doc2vecモデル学習
print('===== Doc2vec =====')
print('training english model...')
en_doc2vec_model = Doc2Vec(en_train_docs, vector_size=300, window=10, min_count=5, workers=4)
print('Training english model Finished!')
print('training japanese model...')
ja_doc2vec_model = Doc2Vec(ja_train_docs, vector_size=300, window=10, min_count=5, workers=4)
print('Training japanese model Finished!')
print('\n')

#Word2vecモデル学習
print('===== Word2vec =====')
print('training english model...')
en_word2vec_model = Word2Vec(sentences=en_train_list, vector_size=100, window=5, min_count=1, workers=4)
print('Training english model Finished!')
print('training japanese model...')
ja_word2vec_model = Word2Vec(sentences=ja_train_list, vector_size=100, window=5, min_count=1, workers=4)
print('Training japanese model Finished!')
print('\n')

#tf-idf学習(今回は使わなかったが使う場合は使ってください)
# print('===== tf-idf =====')
# print('training english model...')
# en_dct = Dictionary(en_train_list) #ID辞書生成
# en_tfidf_corpus = list(map(en_dct.doc2bow, en_train_list)) #コーパスの単語をID化
# en_tfidf_model = TfidfModel(en_tfidf_corpus) #tfidfモデル生成
# en_tfidf_result_ids = en_tfidf_model[en_tfidf_corpus] #コーパスへモデル適用
# print('Training english model Finished!')
# print('training japanese model...')
# ja_dct = Dictionary(ja_train_list) #ID辞書生成
# ja_tfidf_corpus = list(map(ja_dct.doc2bow, ja_train_list)) #コーパスの単語をID化
# ja_tfidf_model = TfidfModel(ja_tfidf_corpus) #tfidfモデル生成
# ja_tfidf_result_ids = ja_tfidf_model[ja_tfidf_corpus] #コーパスへモデル適用
# print('Training japanese model Finished!')
# print('\n')

print('Saving models...')

#Doc2vecモデル保存
en_doc2vec_model.save('model/en_doc2vec.model')
ja_doc2vec_model.save('model/ja_doc2vec.model')


#Word2vecモデル保存
# en_word2vec_model.save('model/en_word2vec.model')
# ja_word2vec_model.save('model/ja_word2vec.model')
en_word2vec_model.wv.save_word2vec_format('model/en_word2vec.bin', binary=True)
ja_word2vec_model.wv.save_word2vec_format('model/ja_word2vec.bin', binary=True)


print('Finished saving all models...')

#テスト
test_class_ids = ['11610212', '30562111', '51100303']
check_list = ['major', 'name', 'summary', 'url']


# for test_class_id in test_class_ids:
#     print("================================================================")
#     print('class_id :', test_class_id)
#     for tmp_check in check_list:
#         print(tmp_check, ' :', ref_data[test_class_id][tmp_check])
#     print('----------------------------------------------------------------')
#     #類似講義
#     tmp_similar_list = en_doc2vec_model.docvecs.most_similar(test_class_id)[:500]
#     for similar_class in tmp_similar_list:
#         similar_class_id = similar_class[0]
#         print(ja_word2vec_model.wmdistance(ja_data[test_class_id].split(' '), ja_data[similar_class_id].split(' ')))
#         exit()
#         similar_class_level = similar_class[1]
#         print('class_id :', similar_class_id, 'similar_level :', similar_class_level)
#         for tmp_check in check_list:
#             print(tmp_check, ' :', ref_data[similar_class_id][tmp_check])
#         print('----------------------------------------------------------------')
    
#     print('\n')

# for test_class_id in test_class_ids:
#     print("================================================================")
#     print('class_id :', test_class_id)
#     for tmp_check in check_list:
#         print(tmp_check, ' :', ref_data[test_class_id][tmp_check])
#     print('----------------------------------------------------------------')
#     #類似講義
#     tmp_similar_list = en_doc2vec_model.docvecs.most_similar(test_class_id)[:10]
#     for similar_class in tmp_similar_list:
#         similar_class_id = similar_class[0]
#         similar_class_level = similar_class[1]
#         print('class_id :', similar_class_id, 'similar_level :', similar_class_level)
#         for tmp_check in check_list:
#             print(tmp_check, ' :', ref_data[similar_class_id][tmp_check])
#         print('----------------------------------------------------------------')
    
#     print('\n')