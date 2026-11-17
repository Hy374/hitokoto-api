# 一言接口(Hitokoto API)

用 Python + FastAPI 写的每日一言接口，访问即返回一句随机名言。

## 功能
- 提供 /hitokoto 接口，返回随机名言、出处、作者
- 带异常处理，接口失败时返回友好错误提示
- 调用 DeepSeek 大模型，对名言自动生成一句 AI 解读

## 技术栈
- Python、FastAPI、requests

## 如何运行
1.安装依赖：pip install fastapi uvicorn requests
2.启动：uvicorn main:app --reload
3.访问：http://127.0.0.1:8000/hitokoto

# 接口说明
GET /hitokoto  →  返回 {"hitokoto":"...","from":"...","from_who":"...","ai_comment":"..."}
