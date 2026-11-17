import requests

resp = requests.get('https://v1.hitokoto.cn/')
print(resp.status_code)
data = resp.json()
print(data['hitokoto'])
# 写一个脚本，统计一句话里每个单词出现的次数，打印出来。比如：
# text = "to be or not to be"
# 期望输出（顺序无所谓）：
# to: 2
# be: 2
# or: 1
# not: 1

def word_count(text):
    word_count_dict = {}
    for word in text.split():
        if word not in word_count_dict:
            word_count_dict[word] = 1
        else:
            word_count_dict[word] += 1
    return word_count_dict

with open('sample.txt', 'r', encoding='utf-8') as f:
    content = f.read()
print(word_count(content))



