
"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : excel_data
@File : test.py
@Author : 帅张张
@Time : 2024/7/4 9:39

"""
import subprocess

def is_process_running(process_name_part):
    try:
        # 调用 tasklist 命令获取所有正在运行的进程列表
        tasklist = subprocess.check_output("tasklist", shell=True, text=True)
        # 检查目标进程名称部分是否在 tasklist 输出中
        if process_name_part.lower() in tasklist.lower():
            print(tasklist.lower())
        return process_name_part.lower() in tasklist.lower()
    except subprocess.CalledProcessError:
        return False

# 测试
process_name_part = "GTJ2025"  # 只需提供进程名的部分，例: "example"
if is_process_running(process_name_part):
    print(f"包含 '{process_name_part}' 的进程正在运行")
else:
    print(f"没有包含 '{process_name_part}' 的进程在运行")