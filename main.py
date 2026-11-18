import requests
import sqlite3
from fastapi.responses import HTMLResponse
from datetime import datetime
from fastapi import FastAPI, Form
from config import API_KEY

app = FastAPI()

# 调用大模型
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

# 存入数据库
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

@app.get("/")
def index():
    # 获取历史记录
    history = get_history()

    items = ""
    # 遍历历史记录，拼接字符串
    for r in history:
        items += f"<li><b>{r['hitokoto']}</b>（{r['source']}）<br>{r['ai_comment']}</li>"
    # 网页结构
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>一言AI解读</title></head>
<body>
    <h1>一言AI解读</h1>
    <form action="/explain" method="post">
        <input type="text" name="text" placeholder="输入一句你想解读的话" size="40">
        <button type="submit">解读</button>
    </form>
    <p>访问 <a href="/hitokoto">/hitokoto</a>随机生成名言+AI解读</p>
    <hr>
    <h2>历史记录(共{len(history)}条)</h2>
    <ul>{items}</ul>
</body>
</html>"""
    # 渲染页面
    return HTMLResponse(html)

@app.post("/explain")
def explain(text: str = Form("")):
    text = text.strip()
    if text == '':
        return HTMLResponse("<p>输入不能为空，请重新输入。</p><p><a href='/'>返回首页</a></p>")
    if len(text) > 200:
        return HTMLResponse("<p>输入太长，请控制在 200 字以内。</p><p><a href='/'>返回首页</a></p>")

    try:
        comment = ask_deepseek(text)
        save_quote(text, "用户输入", None, comment)
    except Exception as e:
        return HTMLResponse(f"<p>解读失败：{e}</p><p><a href='/'>返回首页</a></p>")

    html = f"""<!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>解读结果</title></head>
    <body>
        <h1>解读结果</h1>
        <h2>{text}</h2>
        <p><b>AI 解读：</b>{comment}</p>
        <p><a href="/">再试一句</a></p>
    </body>
    </html>"""
    return HTMLResponse(html)

@app.get("/hitokoto")
def get_hitokoto(text: str = None):
    try:
        if text:
            # 用户传了句子，就解读这句
            quote = text
            source = "用户输入"
            author = None
        else:
            # 没传，就随机拿一句名言
            resp = requests.get('https://v1.hitokoto.cn/')
            data = resp.json()
            quote = data['hitokoto']
            source = data['from']
            author = data['from_who']

        comment = ask_deepseek(quote)
        save_quote(quote, source, author, comment)
        return {
            "hitokoto": quote,
            "from": source,
            "from_who": author,
            "ai_comment": comment
        }
    except Exception as e:
        return {"error":f"接口调用失败:{e}"}

@app.get("/history")
def history():
    return get_history()



if __name__ == "__main__": # 只有运行这个文件才会执行
    import os
    import uvicorn
    # host="0.0.0.0" -> 让服务对外可访问(0.0.0.0 是所有人都能访问)
    # port=int(os.environ.get("PORT", 8000)) -> 端口从环境变量PORT读，没有就用8000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

