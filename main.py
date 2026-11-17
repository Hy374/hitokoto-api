import requests
from fastapi import FastAPI
from config import API_KEY

app = FastAPI()

def ask_deepseek(quote):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization":f"Bearer {API_KEY}",
        "Content-Type":"application/json"
    }
    body = {
        "model":"deepseek-chat",
        "messages":[
            {"role":"system","content":"你是一位擅长解读名言的老师。"},
            {"role":"user","content":f"请用一句话解读这句名言:{quote}"}
        ]
    }
    resp = requests.post(url,headers=headers,json=body)
    data = resp.json()
    return data["choices"][0]["message"]["content"]

@app.get("/hitokoto")
def get_hitokoto():
    try:
        resp = requests.get('https://v1.hitokoto.cn/')
        data = resp.json()
        quote = data['hitokoto']
        comment = ask_deepseek(quote)
        return {
            "hitokoto": quote,
            "from": data['from'],
            "from_who": data['from_who'],
            "ai_comment": comment
        }
    except Exception as e:
        return {"error": f"接口调用失败:{e}"}

