import requests
from config import API_KEY

url = "https://api.deepseek.com/chat/completions"
# 请求头
headers = {
    "Authorization":f"Bearer {API_KEY}", # 身份认证
    "Content-type":"application/json"
}
# 请求体
body = {
    "model":"deepseek-chat",
    "messages":[
        # system是"给模型定的角色"
        {"role":"system","content":"你是以为擅长解读名言的老师。"},
        # user是"你真正说的话"
        {"role":"user","content":"请用一句话解读这句名言：绿树阴浓夏长日，楼台倒影入池塘。"}
    ],
}

# post是"提交数据给服务器处理"
resp = requests.post(url,headers=headers,json=body)
data = resp.json()
# print(data["choices"][0]["message"]["content"])
print(data)