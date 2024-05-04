import os
import json

def replace_in_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 替换 JSON 数据
    def replace_recursively(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    replace_recursively(value)
                elif isinstance(value, str):
                    obj[key] = value.replace("https://zkitefly.github.io/unlisted-versions-of-minecraft/", "https://gitee.com/bleaker/unlisted-versions-of-minecraft/raw/gitee/")
        elif isinstance(obj, list):
            for i in range(len(obj)):
                if isinstance(obj[i], (dict, list)):
                    replace_recursively(obj[i])
                elif isinstance(obj[i], str):
                    obj[i] = obj[i].replace("https://zkitefly.github.io/unlisted-versions-of-minecraft/", "https://gitee.com/bleaker/unlisted-versions-of-minecraft/raw/gitee/")
    
    replace_recursively(data)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def process_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            if item.endswith('.json'):
                replace_in_json(item_path)
        elif os.path.isdir(item_path):
            process_directory(item_path)

# 要处理的文件夹路径
directory_path = 'files'

# 执行递归处理
process_directory(directory_path)

print("替换完成！")
