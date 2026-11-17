# 项目1：做一个【每日一言日报】
# 定位一句话：把你已经会的东西，串成一个真实的小工具——每天调接口拿一句名言，追加1存进一个日报文件。

# 1.拿今天的日期，格式像2026-11-17
# 2.调一言接口拿名言
# 3.把"日期|名言(来源)"拼成一行
# 4.用追加模式写进 daily_lig.txt

import requests
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

try:
    response = requests.get('https://v1.hitokoto.cn/')
    data = response.json()
# 拼接字符串
    line = f"{today}|{data['hitokoto']}({data['from']})"
except Exception as e:
    print("接口调用失败，请检查网络。错误：",e)
else:
    with open('daily_log.txt', 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    print("已写入：",line)




