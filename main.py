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
BASE_URL = f'https://zkitefly.github.io/unlisted-versions-of-minecraft/{FILES_DIR}'

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

    # 处理 2point0_blue 2point0_red 2point0_purple 时间相同问题
    if time == "2013-08-06T06:00:00-05:00" and releaseTime == "2013-03-20T05:00:00-05:00" and id == "2point0_blue":
        releaseTime = "2013-03-20T05:00:02-05:00"
        time = "2013-08-06T06:00:02-05:00"
    if time == "2013-08-06T06:00:00-05:00" and releaseTime == "2013-03-20T05:00:00-05:00" and id == "2point0_red":
        releaseTime = "2013-03-20T05:00:01-05:00"
        time = "2013-08-06T06:00:01-05:00"
    # if time == "2013-08-06T06:00:00-05:00" and releaseTime == "2013-03-20T05:00:00-05:00" and id == "2point0_purple":


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
    
    # 根据 releaseTime 属性降序排序 versions 列表
    manifest_data['versions'] = sorted(manifest_data['versions'], key=lambda x: x['releaseTime'], reverse=True)
    
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
        download_file("https://cfp.zkitefly.eu.org/" + url, json_filename)
        
        # 下载 JAR 文件并保存
        jar_filename = os.path.join(folder_path, f'{id}.jar')
        download_file("https://cfp.zkitefly.eu.org/" + jar_url, jar_filename)
        
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
                # print(f'Converting releaseTime for {id}...')
                releaseTime = iso8601_format(releaseTime)
                json_data['releaseTime'] = releaseTime
            
            if 'T' not in time:
                # print(f'Converting time for {id}...')
                time = iso8601_format(time)
                json_data['time'] = time
            
            # 检查是否存在 downloads 属性，如果不存在则添加
            if 'downloads' not in json_data:
                json_data['downloads'] = {}

            # 检查是否存在 client 属性，如果不存在则添加
            if 'client' not in json_data['downloads']:
                sha1 = snapshot['sha1']
                size = snapshot['size']
                json_data['downloads']['client'] = {
                    'sha1': sha1,
                    'size': size,
                    'url': f'{BASE_URL}/{id}/{id}.jar'
                }
            
            json_data['libraries'] += {
                "name": "com.zero:retrowrapper:1.7.8",
                "downloads": {
                    "artifact": {
                        "path": "com/zero/retrowrapper/1.7.8/RetroWrapper-1.7.8.jar",
                        "url": "https://zkitefly.github.io/unlisted-versions-of-minecraft/libraries/RetroWrapper-1.7.8.jar",
                        "sha1": "ea9175b4aebe091ae8859f7352fe59077a62bdf4",
                        "size": 181263
                    }
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
        download_file("https://cfp.zkitefly.eu.org/" + url, json_filename)
        
        # 下载 JAR 文件并保存
        jar_filename = os.path.join(folder_path, f'{id}.jar')
        download_file("https://cfp.zkitefly.eu.org/" + jar_url, jar_filename)
        
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
                # print(f'Converting releaseTime for {id}...')
                releaseTime = iso8601_format(releaseTime)
                json_data['releaseTime'] = releaseTime
            
            if 'T' not in time:
                # print(f'Converting time for {id}...')
                time = iso8601_format(time)
                json_data['time'] = time
            
            # 检查是否存在 downloads 属性，如果不存在则添加
            if 'downloads' not in json_data:
                json_data['downloads'] = {}

            # 检查是否存在 client 属性，如果不存在则添加
            if 'client' not in json_data['downloads']:
                sha1 = other_versions['sha1']
                size = other_versions['size']
                json_data['downloads']['client'] = {
                    'sha1': sha1,
                    'size': size,
                    'url': f'{BASE_URL}/{id}/{id}.jar'
                }
            
            # 如果 fid 是指定的值，添加数据
            if fid in ["2point0_blue", "2point0_purple", "2point0_red"]:
                json_data['assetIndex'] = {
                    "id": "pre-1.6",
                    "sha1": "4759bad2824e419da9db32861fcdc3a274336532",
                    "size": 73813,
                    "totalSize": 49381897,
                    "url": "https://launchermeta.mojang.com/v1/packages/4759bad2824e419da9db32861fcdc3a274336532/pre-1.6.json"
                }
                json_data['assets'] = "pre-1.6"

            # 如果 id 是特定值，则替换特定的 URL
            if fid == "a1.1.1":
                json_string = json.dumps(json_data)
                json_string = json_string.replace("https://files.betacraft.uk/launcher/assets/lwjgl-2.9.3-grayscreenfix.jar", "https://zkitefly.github.io/unlisted-versions-of-minecraft/libraries/lwjgl-2.9.3-grayscreenfix.jar")
                json_data = json.loads(json_string)

            # 处理 c0.28_01 的日月颠倒问题
            if time == "2017-20-09T03:19:48+01:00" and releaseTime == "2009-27-10T00:00:00+00:00" and id == "c0.28_01":
                time = "2017-09-20T03:19:48+01:00"
                releaseTime = "2009-10-27T00:00:00+00:00"
                json_data['time'] = time
                json_data['releaseTime'] = releaseTime

            json_data['libraries'] += {
                "name": "com.zero:retrowrapper:1.7.8",
                "downloads": {
                    "artifact": {
                        "path": "com/zero/retrowrapper/1.7.8/RetroWrapper-1.7.8.jar",
                        "url": "https://zkitefly.github.io/unlisted-versions-of-minecraft/libraries/RetroWrapper-1.7.8.jar",
                        "sha1": "ea9175b4aebe091ae8859f7352fe59077a62bdf4",
                        "size": 181263
                    }
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
        download_file("https://cfp.zkitefly.eu.org/" + url, zip_filename)
        
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
