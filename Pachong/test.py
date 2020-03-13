from typing import List
import json

if __name__ == '__main__':
    data = {
        'no': 1,
        'name': 'Runoob',
        'url': 'http://www.runoob.com',
        'dic':[
        {"name":"jin"},{"m":"ddd"}
        ]
    }
    #json 字符串
    json_str = json.dumps(data)
    # 将 JSON 对象转换为 Python 字典
    data2 = json.loads(json_str)
    print(data2["dic"])


