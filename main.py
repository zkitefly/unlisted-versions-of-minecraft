import os
import requests
import json
import zipfile
from datetime import datetime
import time

# 文件基础 URL
BASE_URL = 'https://zkitefly.github.io/unlisted-versions-of-minecraft/files'

def download_file(url, filename, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            with open(filename, 'wb') as f:
                response = requests.get(url)
                response.raise_for_status()  # 检查响应状态码
                f.write(response.content)
                return  # 如果下载成功，则直接返回
        except Exception as e:
            print(f'Download failed: {e}')
            retries += 1
            if retries < max_retries:
                print(f'Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)
            else:
                print('Max retries exceeded, giving up...')
                raise  # 如果超过最大重试次数，则抛出异常

    return  # 如果下载成功，则直接返回

def iso8601_format(timestamp_str):
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
    return timestamp.isoformat() + 'Z'

def update_version_manifest(id, releaseTime_str, time_str, type):
    releaseTime = iso8601_format(releaseTime_str)
    time = iso8601_format(time_str)
    manifest_filename = 'version_manifest.json'
    if os.path.exists(manifest_filename):
        with open(manifest_filename, 'r') as f:
            manifest_data = json.load(f)
    else:
        manifest_data = {'versions': []}
    
    new_version = {
        'id': id,
        'type': type,
        'url': f'{BASE_URL}/{id}/{id}.json',
        'jar': f'{BASE_URL}/{id}/{id}.jar',
        'time': time,
        'releaseTime': releaseTime
    }
    
    manifest_data['versions'].append(new_version)
    
    with open(manifest_filename, 'w') as f:
        json.dump(manifest_data, f, indent=4)

def main():
    # 处理 old_snapshots.json
    with open('mojang-minecraft-old-snapshots.json', 'r') as f:
        old_snapshots_data = json.load(f)
    
    # 处理 experiments.json
    with open('mojang-minecraft-experiments.json', 'r') as f:
        experiments_data = json.load(f)
    
    # 创建文件夹
    if not os.path.exists('files'):
        os.makedirs('files')
    
    # 处理 old_snapshots 列表
    for snapshot in old_snapshots_data['old_snapshots']:
        id = snapshot['id'].replace('_', '.')  # 将 "_" 替换为 "."
        url = snapshot['url']
        jar_url = snapshot['jar']
        
        # 创建以 id 命名的文件夹
        folder_path = os.path.join('files', id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 下载 JSON 文件并保存
        json_filename = os.path.join(folder_path, f'{id}.json')
        download_file(url, json_filename)
        
        # 下载 JAR 文件并保存
        jar_filename = os.path.join(folder_path, f'{id}.jar')
        download_file(jar_url, jar_filename)
        
        print(f'Downloaded {id}.json and {id}.jar')
        
        # 读取 JSON 文件并更新 version_manifest.json
        with open(json_filename, 'r') as f:
            json_data = json.load(f)
            releaseTime = json_data['releaseTime']
            time = json_data['time']
            type = json_data['type']
            update_version_manifest(id, releaseTime, time, type)
    
    # 处理 experiments 列表
    for experiment in experiments_data['experiments']:
        id = experiment['id']
        url = experiment['url']
        
        # 创建以 id 命名的文件夹
        folder_path = os.path.join('files', id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 下载 ZIP 文件并保存
        zip_filename = os.path.join(folder_path, f'{id}.zip')
        download_file(url, zip_filename)
        
        # 解压 ZIP 文件并提取 JSON 文件
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extract(f'{id}/{id}.json', folder_path)
        
        # 删除 ZIP 文件
        os.remove(zip_filename)
        
        print(f'Downloaded and extracted {id}.json from ZIP file')
        
        # 读取 JSON 文件并更新 version_manifest.json
        json_filename = os.path.join(folder_path, f'{id}.json')
        with open(json_filename, 'r') as f:
            json_data = json.load(f)
            releaseTime = json_data['releaseTime']
            time = json_data['time']
            type = json_data['type']
            update_version_manifest(id, releaseTime, time, type)

if __name__ == "__main__":
    main()