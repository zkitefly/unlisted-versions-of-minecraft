import json
import os
import platform
import urllib.request
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def get_default_export_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.getenv('APPDATA'), ".minecraft")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/minecraft")
    elif system == "Linux":
        return os.path.expanduser("~/.minecraft")
    else:
        return None

def choose_export_path():
    export_path = filedialog.askdirectory()
    export_entry.delete(0, tk.END)
    export_entry.insert(0, export_path)

def download_selected_version():
    selected_item = versions_tree.selection()
    if selected_item:
        item = versions_tree.item(selected_item)
        version_id = item['values'][0]
        url = item['values'][2]
        export_path = export_entry.get()
        versions_folder = os.path.join(export_path, "versions", version_id)
        os.makedirs(versions_folder, exist_ok=True)
        download_file(version_id, url, versions_folder)

def download_file(version_id, url, download_path):
    file_name = version_id
    full_path = os.path.join(download_path, file_name)
    urllib.request.urlretrieve(url, full_path)
    status_label.config(text=f"下载完成 {file_name} 到 {download_path}")

def fetch_versions():
    version_manifest = "https://zkitefly.github.io/unlisted-versions-of-minecraft/version_manifest.json"
    with urllib.request.urlopen(version_manifest) as response:
        data = json.loads(response.read().decode())
        versions = data["versions"]
        for version in versions:
            id = version["id"]
            type = version["type"]
            url = version["url"]
            release_time = version["releaseTime"]
            versions_tree.insert("", "end", values=(id, type, url, release_time))

# 创建主窗口
root = tk.Tk()
root.title("unlisted-versions-of-minecraft 版本下载器 - v1.2")

# 创建下载路径输入框和按钮
export_frame = ttk.Frame(root)
export_frame.pack(pady=10)
export_label = ttk.Label(export_frame, text="导出路径:")
export_label.grid(row=0, column=0)
export_default_path = get_default_export_path()
export_entry = ttk.Entry(export_frame, width=40)
export_entry.insert(0, export_default_path)
export_entry.grid(row=0, column=1, padx=5)
browse_button = ttk.Button(export_frame, text="浏览", command=choose_export_path)
browse_button.grid(row=0, column=2)

# 创建版本列表
versions_tree = ttk.Treeview(root, columns=("ID", "类型", "URL", "发布时间"), show="headings")
versions_tree.heading("ID", text="ID")
versions_tree.heading("类型", text="类型")
versions_tree.heading("URL", text="URL")
versions_tree.heading("发布时间", text="发布时间")
versions_tree.pack(padx=10, pady=5, fill="both", expand=True)

# 加载版本列表数据
fetch_versions()

# 创建下载按钮
download_button = ttk.Button(root, text="下载选定版本", command=download_selected_version)
download_button.pack(pady=5)

# 创建状态标签
status_label = ttk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()
