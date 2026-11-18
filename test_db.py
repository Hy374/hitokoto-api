import sqlite3

# 1.链接数据库（文件不存在会自动创建）
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 2.建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hitokoto TEXT,
    ai_comment TEXT
)
''')

# 3.插入一条数据
cursor.execute(
    'INSERT INTO quotes (hitokoto, ai_comment) VALUES (?, ?)',
    ('测试名言', '测试解读')
)
conn.commit()

# 4.查询所有数据
cursor.execute('SELECT * FROM quotes')
rows = cursor.fetchall()
print(rows)

conn.close()