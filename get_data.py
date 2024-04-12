import re

import pandas as pd

# 假设的文件路径
file_path = './html_data.text'

# 准备用于匹配双色球信息的正则表达式
pattern = re.compile(
    r'(\d{7})双色球开机号码：红球：(\d{2}),(\d{2}),(\d{2}),(\d{2}),(\d{2}),(\d{2}) 蓝球：(\d{2}) 开奖号：(\d{2}) (\d{2}) (\d{2}) (\d{2}) (\d{2}) (\d{2}) \+ (\d{2})')

# 用于存储提取的数据
lottery_data = []

# 读取文件并提取数据
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  # 读取整个文件内容
    matches = pattern.finditer(content)  # 在整个文件内容中寻找所有匹配
    for match in matches:
        data = {
            '期号': match.group(1),
            '开奖红球号码': match.groups()[8:14],
            '开奖蓝球号码': match.group(15)
        }
        lottery_data.append(data)

df = pd.DataFrame(lottery_data)

# 将DataFrame保存为CSV文件
file_path = "./lottery_data.csv"
df.to_csv(file_path, index=False)