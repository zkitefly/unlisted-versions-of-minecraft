import requests
import os
import hashlib

def get_file_info(url):
    try:
        # 发送 GET 请求获取文件内容
        response = requests.get(url)
        
        if response.status_code == 200:
            # 获取文件名
            filename = url.split('/')[-1]
            
            # 保存文件
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # 计算文件大小
            file_size = os.path.getsize(filename)
            
            # 计算 SHA1 值
            sha1_hash = hashlib.sha1()
            with open(filename, 'rb') as f:
                # 分块读取文件，适用于大文件
                for chunk in iter(lambda: f.read(4096), b""):
                    sha1_hash.update(chunk)
            
            # 获取链接 ID
            id = url.split('/')[-1].replace('.jar', '')

            # 输出文件大小和 SHA1 值
            print(f"文件大小: {file_size} 字节")
            print(f"SHA1 值: {sha1_hash.hexdigest()}")
            print(f"ID: {id}")
            
            # 删除文件
            os.remove(filename)
            print("文件已删除")
        else:
            print("无法获取文件")
    except Exception as e:
        print(f"发生异常: {e}")

if __name__ == "__main__":
    while True:
        url = input("请输入链接 (输入 'exit' 退出程序): ")
        if url.lower() == 'exit':
            break
        get_file_info(url)
