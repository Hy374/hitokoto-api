import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/hitokoto")
def get_hitokoto():
    try:
        resp = requests.get('https://v1.hitokoto.cn/')
        data = resp.json()
        return {
            "hitokoto": data['hitokoto'],
            "from": data['from'],
            "from_who": data['from_who']
        }
    except Exception as e:
        return {"error": f"接口调用失败:{e}"}

