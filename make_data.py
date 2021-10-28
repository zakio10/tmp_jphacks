import json
import glob
import MeCab
import re
import tqdm
import nltk as en_tokenizer

#読み込み用
data = dict()

#参照用データ
ref_data = dict()
ref_list = ['preiod', 'degree', 'major', 'name', 'url', 'place', 'num_credits', 'day']

#記号削除定義
code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・•—–◆●■□◇（）＄＃＠。、：；？！／〜｀＋￥％，．①②③④⑤⑥⑦⑧⑨]') #記号
number_regex = re.compile('[0-9]|[０-９]') #数字
korean_regex = re.compile('[\uac00-\ud7af\u3200-\u321f\u3260-\u327f\u1100-\u11ff\u3130-\u318f\uffa0-\uffdf\ua960-\ua97f\ud7b0-\ud7ff]+[\\s\.,]*') #韓国語

#Tokenizer定義(英語)
# en_tokenizer = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/ -Owakati')

#Tokenizer定義(日本語)
ja_tokenizer = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')

#jsonファイル読み込み
with open('data/2021.json', mode='r') as f:
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

#日本語講義
ja_corpus_data = dict()
ja_posid_data = dict()

#英語講義
en_corpus_data = dict()
en_posid_data = dict()


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
        #参照用データ作成用
        tmp_ref_data = dict()

        #class_idには講義ID
        #tmp_class_dataには現在，取り出しているある1つの講義dictが格納
        tmp_class_data = data[data_key][class_id]
        
        #参照用
        for tmp_ref_content in ref_list:
            tmp_ref_data[tmp_ref_content] = tmp_class_data[tmp_ref_content]
        tmp_ref_data['group'] = data_key

        #講義データから概要，到達目標，スケジュールが含まれる項目を取り出す
        tmp_class_data = tmp_class_data['syllabus_contents']

        #参照用
        tmp_ref_data['summary'] = tmp_class_data['summary']

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
            # tmp_corpus_data =  tmp_corpus_data.rstrip("n","")
            # tmp_corpus_data =  tmp_corpus_data.rstrip("\\","")
            tmp_corpus_data =  tmp_corpus_data.rstrip().replace('\n', ' ').replace('\u3000', '').replace('’s', '').replace('’', '').replace('‘', '')
            tmp_corpus_data = code_regex.sub('', tmp_corpus_data)
            tmp_corpus_data = number_regex.sub('', tmp_corpus_data)
            tmp_corpus_data = korean_regex.sub('', tmp_corpus_data)
            #教員名削除
            for instructor in instructors:
                tmp_corpus_data =  tmp_corpus_data.replace(instructor, '')
        except TypeError as e:
            print('No data: ', class_id)
            tmp_corpus_data = ""


        # #現在注目しているデータが英語科日本語かチェック(文字列がASCII文字か判定)
        # if tmp_corpus_data.isascii() == True:
        #     # print(tmp_corpus_data)
        #     #英語分かち書き
        #     tmp_corpus_data = ' '.join(en_tokenizer.word_tokenize(tmp_corpus_data))
        #     #英語コーパスデータに追加
        #     en_corpus_data[class_id] = tmp_corpus_data
        # else:
        #     #日本語分かち書き
        #     tmp_corpus_data = ja_tokenizer.parse(tmp_corpus_data)
        #     tmp_corpus_data = tmp_corpus_data.replace(' \n', '')
        #     #日本語コーパスデータに追加
        #     ja_corpus_data[class_id] = tmp_corpus_data

        #アスキー文字抽出
        if tmp_corpus_data:
            ascii_str = re.sub(r'[^!-~\\s]|[　]', '',tmp_corpus_data)
            # print(ascii_str)
            #アスキー文字が7割以上のとき英語と判定
            if len(ascii_str) / len(tmp_corpus_data) > 0.7:
            # #現在注目しているデータが英語科日本語かチェック(文字列がASCII文字か判定)
            # if tmp_corpus_data.isascii() == True:
                # print(tmp_corpus_data)
                #アスキー文字以外を消去
                # tmp_corpus_data = ascii_str
                #品詞格納用リスト
                tmp_posid_data = []
                #英語分かち書き
                tmp_corpus_data = en_tokenizer.word_tokenize(tmp_corpus_data) #形態素解析
                tmp_posid_data = en_tokenizer.pos_tag(tmp_corpus_data) #品詞取得
                if len(tmp_corpus_data) != len(tmp_posid_data):
                    print("エラー : 品詞と形態素の個数が異なる!")
                tmp_corpus_data = ' '.join(tmp_corpus_data) #形態素解析結果連結
                tmp_posid_data = [p[1] for p in tmp_posid_data]
                #英語コーパスデータに追加
                en_corpus_data[class_id] = tmp_corpus_data
                en_posid_data[class_id] = tmp_posid_data
            else:
                #日本語分かち書き
                node = ja_tokenizer.parseToNode(tmp_corpus_data)
                tmp_corpus_data = []
                tmp_posid_data = []
                while node:
                    if node.feature.split(',')[0] == '記号':
                        node = node.next
                    tmp_corpus_data.append(node.surface) #形態素保存
                    tmp_posid_data.append(node.feature.split(',')[0]) #品詞保存
                    node = node.next
                
                del tmp_corpus_data[0] #文頭(BOS)削除
                del tmp_corpus_data[-1] #文末(EOS)削除
                del tmp_posid_data[0] #文頭(BOS)削除
                del tmp_posid_data[-1] #文末(EOS)削除
                if len(tmp_corpus_data) != len(tmp_posid_data):
                    print("エラー : 品詞と形態素の個数が異なる!")

                tmp_corpus_data = ' '.join(tmp_corpus_data) #形態素のリストを連結
                # tmp_corpus_data = tmp_corpus_data.replace(' \n', '')
                #日本語コーパスデータに追加
                ja_corpus_data[class_id] = tmp_corpus_data
                ja_posid_data[class_id] = tmp_posid_data

        #参照用データ保存
        ref_data[class_id] = tmp_ref_data

        #コーパスデータ保存
        corpus_data[class_id] = tmp_corpus_data


#重複した教員の名前を削除
instructors = list(set(instructors))

#教員名出力用辞書
instructors_data = dict()
instructors_data['instructors'] = instructors

#コーパスjsonファイル出力
with open('data/corpus_data.json', 'w') as f:
    json.dump(corpus_data, f, ensure_ascii=False, indent=4)

#参照用jsonファイル出力
with open('data/ref_data.json', 'w') as f:
    json.dump(ref_data, f, ensure_ascii=False, indent=4)

#言語別コーパス(tf-idf用)
div_corpus_data = dict()
div_corpus_data['en'] = en_corpus_data
div_corpus_data['ja'] = ja_corpus_data

#言語別品詞データ
div_posid_data = dict()
div_posid_data['en'] = en_posid_data
div_posid_data['ja'] = ja_posid_data

#言語別コーパスjsonファイル出力
with open('data/div_corpus_data.json', 'w') as f:
    json.dump(div_corpus_data, f, ensure_ascii=False, indent=4)

#品詞データjsonファイル出力
with open('data/div_posid_data.json', 'w') as f:
    json.dump(div_posid_data, f, ensure_ascii=False, indent=4)

#教員名jsonファイル出力
with open('data/instructors_data.json', 'w') as f:
    json.dump(instructors_data, f, ensure_ascii=False, indent=4)


# for idx, i in enumerate(corpus_data.keys()):
#     if idx <1000:
#         continue
#     print(idx)
#     print(i)
#     print(corpus_data[i])
#     if idx >1010:
#         break