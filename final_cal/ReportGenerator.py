"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : final_cal
@File : ReportGenerator.py
@Author : 帅张张
@Time : 2024/6/11 10:34

"""
import pandas as pd
import os

# ReportGenerator: 负责将汇总结果写入新的Excel文件
class ReportGenerator:
    def generate_report(self, data: pd.DataFrame, output_path: str, file_name: str = ''):
        raise NotImplementedError("Subclasses should implement this generate_report method.")


class SubReport(ReportGenerator):
    def generate_report(self, data: pd.DataFrame, output_path: str, file_name: str = ''):

        data.to_excel(output_path, index=False)


# class ControlTableReport(ReportGenerator):
#     def generate_report(self, data: pd.DataFrame, output_path: str, file_name: str = ''):
#         data.to_excel(os.path.join(output_path, file_name), index=False)
