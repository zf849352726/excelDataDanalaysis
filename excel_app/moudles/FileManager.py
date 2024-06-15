"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : final_cal
@File : FileManager.py
@Author : 帅张张
@Time : 2024/6/11 10:32

"""
import pandas as pd
import os
import re


# FileManager: 负责读取文件夹中的所有Excel文件
class FileManager:
    def __init__(self, directory_paths, keyword):
        self.directory_paths = directory_paths
        self.keyword = keyword

    def get_excel_files(self):
        excel_files = []
        pattern = re.compile(self.keyword)
        for directory_path in self.directory_paths:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.endswith('.xlsx') and pattern.search(file) and not file.startswith('~$'):
                        excel_files.append(os.path.join(root, file))
        return excel_files

    def read_excel(self, file_path, header=0):
        return pd.read_excel(file_path, header=header, engine='openpyxl')

