import json
import glob
import MeCab
import re
import tqdm
import nltk as en_tokenizer

data = dict()

#記号削除定義
code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、：；？！／｀＋￥％，．]')
number_regex = re.compile('[0-9]|[０-９]')

#Tokenizer定義(英語)
# en_tokenizer = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/ -Owakati')

#Tokenizer定義(日本語)
ja_tokenizer = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/ -Owakati')

#jsonファイル読み込み
with open('2021.json', mode='r') as f:
    data = json.load(f)

#keyのリスト(学部の名前)
data_keys_list = list(data.keys())

#講義IDのリストのdict(学部名(キー)を入れると講義IDのリストが返る)
data_ids_dict = dict()

for data_key in data_keys_list:
    data_ids_dict[data_key] =list(data[data_key].keys())

#コーパスデータ(＜概要/Course Content Summary＞ + ＜到達目標/Goals,Aims＞ + ＜授業計画/Schedule＞の（内容/Contents）)
#keyは講義ID
corpus_data = dict()

#教員の名前(ストップワード用)(上の名前と下の名前の間に半角の空白)
instructors = []

print('教員名を読み込み中...')
#教員の名前を格納(ストップワードに利用)
for data_key in tqdm.tqdm(data_keys_list):
    #data_keyにはジャンル格納(例:"2021_学部_理工学部･理工学研究科（工学研究科）")
    for idx, class_id in enumerate(data_ids_dict[data_key]):
        #class_idには講義ID
        #tmp_class_dataには現在，取り出しているある1つの講義dictが格納
        tmp_class_data = data[data_key][class_id]

        #教員の名前を格納(ストップワードに利用)
        try:
            for tmp_instructor in tmp_class_data['instructors']:
                instructors.append(tmp_instructor.replace('\u3000', ' '))
        except KeyError as e:
            print('No instructors: ', class_id)


#重複した教員の名前を削除
instructors = list(set(instructors)) #半角空白
instructors_1 = [s.replace(' ', '') for s in instructors] #連結

#すべての組み合わせのリスト
instructors = instructors + instructors_1


print('コーパスデータ作成中...')
#コーパスデータ作成
for data_key in tqdm.tqdm(data_keys_list):
    #data_keyにはジャンル格納(例:"2021_学部_理工学部･理工学研究科（工学研究科）")
    for idx, class_id in enumerate(data_ids_dict[data_key]):
        #class_idには講義ID
        #tmp_class_dataには現在，取り出しているある1つの講義dictが格納
        tmp_class_data = data[data_key][class_id]

        #教員の名前を格納(ストップワードに利用)
        try:
            for tmp_instructor in tmp_class_data['instructors']:
                instructors.append(tmp_instructor.replace('\u3000', ' '))
        except KeyError as e:
            print('No instructors: ', class_id)
        
        #講義データから概要，到達目標，スケジュールが含まれる項目を取り出す
        tmp_class_data = tmp_class_data['syllabus_contents']

        #現在注目している講義のコーパスデータを一時的に保持するリスト
        tmp_corpus_data = []
        
        #＜概要/Course Content Summary＞
        tmp_corpus_data.append(tmp_class_data['summary'])

        #＜到達目標/Goals,Aims＞
        tmp_corpus_data.append(tmp_class_data['goals'])

        #＜授業計画/Schedule＞の（内容/Contents）
        #講義ID:11502061-002でエラー発生を回避
        try:
            for hoge in tmp_class_data['schedule']:
                tmp_corpus_data.append(hoge['contents'])
        except TypeError as e:
            print('No schedule: ', class_id)
        
        #今まで追加した＜概要/Course Content Summary＞ + ＜到達目標/Goals,Aims＞ + ＜授業計画/Schedule＞の（内容/Contents）を連結
        #講義ID:11502061-002でエラー発生を回避
        try:
            tmp_corpus_data = ' '.join(tmp_corpus_data)
            #不要文字削除または置換
            tmp_corpus_data =  tmp_corpus_data.replace('\n', '').replace('\u3000', '')
            tmp_corpus_data = code_regex.sub('', tmp_corpus_data)
            tmp_corpus_data = number_regex.sub('', tmp_corpus_data)
            #教員名削除
            for instructor in instructors:
                tmp_corpus_data =  tmp_corpus_data.replace(instructor, '')
        except TypeError as e:
            print('No data: ', class_id)
            tmp_corpus_data = "None"


        #現在注目しているデータが英語科日本語かチェック(文字列がASCII文字か判定)
        if tmp_corpus_data.isascii() == True:
            # print(tmp_corpus_data)
            #英語分かち書き
            tmp_corpus_data = ' '.join(en_tokenizer.word_tokenize(tmp_corpus_data))
        else:
            #日本語分かち書き
            tmp_corpus_data = ja_tokenizer.parse(tmp_corpus_data)

        #コーパスデータに追加
        corpus_data[class_id] = tmp_corpus_data


#重複した教員の名前を削除
instructors = list(set(instructors))

#出力用辞書
output_data = dict()

output_data['instructors'] = instructors
output_data['corpus'] = corpus_data

#jsonファイル出力
with open('corpus_data.json', 'w') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)



# for idx, i in enumerate(corpus_data.keys()):
#     if idx <1000:
#         continue
#     print(idx)
#     print(i)
#     print(corpus_data[i])
#     if idx >1010:
#         break