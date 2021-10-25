import json
import glob

file_paths = glob.glob('2021/*.json')

print("test")

# print(file_paths)

data = dict()

for tmp_path in file_paths:
    d = dict()
    with open(tmp_path, mode='r') as f:
        d = json.load(f)
        tmp_d = dict()
        for i in d:
            tmp_d[i['code']] = i
        data[tmp_path.split('/')[1].split('.')[0]] = tmp_d


print(data.keys())

print(type(data))

# print(data['2021_法学部'].keys())

with open('all.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)