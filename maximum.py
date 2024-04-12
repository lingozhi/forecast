import re
from collections import Counter
import itertools
# 假设的文件路径
file_path = './html_data.text'
import pandas as pd
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

# 提取所有红球和蓝球号码
all_reds = list(itertools.chain(*[item['开奖红球号码'] for item in lottery_data]))
all_blues = [item['开奖蓝球号码'] for item in lottery_data]

# 统计每个号码出现的频次
red_freq = Counter(all_reds)
blue_freq = Counter(all_blues)

# 选择出现频次最高的红球和蓝球号码
most_common_reds = [num for num, count in red_freq.most_common(6)]
most_common_blue = blue_freq.most_common(1)[0][0]

print(most_common_reds, most_common_blue)
