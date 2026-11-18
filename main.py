import requests
import sqlite3
from datetime import datetime
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

def save_quote(quote, source, author, comment):
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hitokoto TEXT,
            source TEXT,
            author TEXT,
            ai_comment TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute(
        'INSERT INTO quotes (hitokoto, source, author, ai_comment, created_at) VALUES (?, ?, ?, ?, ?)',
        (quote, source, author, comment, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hitokoto TEXT,
            source TEXT,
            author TEXT,
            ai_comment TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('SELECT id, hitokoto, source, author, ai_comment, created_at FROM quotes ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id":r[0],
            "hitokoto":r[1],
            "source":r[2],
            "author":r[3],
            "ai_comment":r[4],
            "created_at":r[5]
        })
    return result


@app.get("/hitokoto")
def get_hitokoto():
    try:
        resp = requests.get('https://v1.hitokoto.cn/')
        data = resp.json()
        quote = data['hitokoto']
        comment = ask_deepseek(quote)
        save_quote(quote, data['from'], data['from_who'], comment) # 存进数据库
        return {
            "hitokoto": quote,
            "from": data['from'],
            "from_who": data['from_who'],
            "ai_comment": comment
        }
    except Exception as e:
        return {"error": f"接口调用失败:{e}"}


@app.get("/history")
def history():
    return get_history()

