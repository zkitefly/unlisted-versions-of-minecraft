import os
import requests
import json
import zipfile
from datetime import datetime
import time
import shutil

# 文件夹名称
FILES_DIR = 'files'

# 文件基础 URL
BASE_URL = f'https://gitee.com/bleaker/unlisted-versions-of-minecraft/raw/gitee/{FILES_DIR}'

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
    if 'T' in timestamp_str:
        return timestamp_str  # 如果已经是 ISO 8601 格式，则直接返回
    else:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
        return timestamp.isoformat() + '+00:00'

def update_version_manifest(fid, id, releaseTime_str, time_str, type):
    releaseTime = iso8601_format(releaseTime_str)
    time = iso8601_format(time_str)
    manifest_filename = 'version_manifest.json'
    if os.path.exists(manifest_filename):
        with open(manifest_filename, 'r') as f:
            manifest_data = json.load(f)
    else:
        manifest_data = {'versions': []}
    
    new_version = {
        'id': fid,
        'type': type,
        'url': f'{BASE_URL}/{id}/{id}.json',
        'time': time,
        'releaseTime': releaseTime
    }
    
    manifest_data['versions'].append(new_version)
    
    with open(manifest_filename, 'w') as f:
        json.dump(manifest_data, f)
    
    with open("raw-" + manifest_filename, 'w') as f:
        json.dump(manifest_data, f, indent=4)

def main():
    # 删除 version_manifest.json 文件和 files 文件夹（如果存在）
    if os.path.exists('version_manifest.json'):
        os.remove('version_manifest.json')
        print('Deleted existing version_manifest.json')
    if os.path.exists(FILES_DIR):
        shutil.rmtree(FILES_DIR)
        print(f'Deleted existing {FILES_DIR} directory')

    # 处理 old_snapshots.json
    with open('mojang-minecraft-old-snapshots.json', 'r') as f:
        old_snapshots_data = json.load(f)

    # 处理 other_versions.json
    with open('other-versions.json', 'r') as f:
        other_versions_data = json.load(f)
    
    # 处理 experiments.json
    with open('mojang-minecraft-experiments.json', 'r') as f:
        experiments_data = json.load(f)
    
    # 创建文件夹
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    
    # 处理 old_snapshots 列表
    for snapshot in old_snapshots_data['old_snapshots']:
        id = snapshot['id'].replace('~', '-')  # 13w12~ -> 13w12-，因为 GitHub Page 下载不了带 ~ 的东西（搞不懂）
        url = snapshot['url']
        jar_url = snapshot['jar']
        
        # 创建以 id 命名的文件夹
        folder_path = os.path.join(FILES_DIR, id)
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
            fid = json_data['id']
            
            # 检查 releaseTime 和 time 属性是否处于 ISO 8601 格式
            if 'T' not in releaseTime:
                print(f'Converting releaseTime for {id}...')
                releaseTime = iso8601_format(releaseTime)
                json_data['releaseTime'] = releaseTime
            
            if 'T' not in time:
                print(f'Converting time for {id}...')
                time = iso8601_format(time)
                json_data['time'] = time
            
            # 检查是否存在 downloads 属性，如果不存在则添加
            if 'downloads' not in json_data:
                sha1 = snapshot['sha1']
                size = snapshot['size']
                json_data['downloads'] = {
                    'client': {
                        'sha1': sha1,
                        'size': size,
                        'url': f'{BASE_URL}/{id}/{id}.jar'
                    }
                }
                # 保存更新后的 JSON 文件
                with open(json_filename, 'w') as json_file:
                    json.dump(json_data, json_file)
            
            update_version_manifest(fid, id, releaseTime, time, type)

    # 处理 other_versions 列表
    for other_versions in other_versions_data['other_versions']:
        id = other_versions['id']
        url = other_versions['url']
        jar_url = other_versions['jar']
        
        # 创建以 id 命名的文件夹
        folder_path = os.path.join(FILES_DIR, id)
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
            fid = json_data['id']
            
            # 检查 releaseTime 和 time 属性是否处于 ISO 8601 格式
            if 'T' not in releaseTime:
                print(f'Converting releaseTime for {id}...')
                releaseTime = iso8601_format(releaseTime)
                json_data['releaseTime'] = releaseTime
            
            if 'T' not in time:
                print(f'Converting time for {id}...')
                time = iso8601_format(time)
                json_data['time'] = time
            
            # 检查是否存在 downloads 属性，如果不存在则添加
            if 'downloads' not in json_data:
                sha1 = other_versions['sha1']
                size = other_versions['size']
                json_data['downloads'] = {
                    'client': {
                        'sha1': sha1,
                        'size': size,
                        'url': f'{BASE_URL}/{id}/{id}.jar'
                    }
                }
                # 保存更新后的 JSON 文件
                with open(json_filename, 'w') as json_file:
                    json.dump(json_data, json_file)
            
            update_version_manifest(fid, id, releaseTime, time, type)
    
    # 处理 experiments 列表
    for experiment in experiments_data['experiments']:
        id = experiment['id']
        url = experiment['url']
        
        # 创建以 id 命名的文件夹
        folder_path = os.path.join(FILES_DIR, id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 下载 ZIP 文件并保存
        zip_filename = os.path.join(folder_path, f'{id}.zip')
        download_file(url, zip_filename)
        
        # 解压 ZIP 文件并提取 JSON 文件
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extract(f'{id}/{id}.json', FILES_DIR)
        
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
            update_version_manifest(id, id, releaseTime, time, type)

if __name__ == "__main__":
    main()
