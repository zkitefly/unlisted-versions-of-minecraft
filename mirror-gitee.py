import os

def replace_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 进行替换
    content = content.replace('https://zkitefly.github.io/unlisted-versions-of-minecraft/', 'https://gitee.com/bleaker/unlisted-versions-of-minecraft/raw/gitee/')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def recursive_replace(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isdir(item_path):
            recursive_replace(item_path)
        elif item.endswith('.json'):
            replace_in_file(item_path)

# 当前目录
current_dir = os.getcwd()
recursive_replace(current_dir)
print("替换完成！")
