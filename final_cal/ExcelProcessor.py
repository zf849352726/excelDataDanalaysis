"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : final_cal
@File : ExcelProcessor.py
@Author : 帅张张
@Time : 2024/6/11 10:32

"""
from final_cal.FilterStrategy import FilterStrategy
from final_cal.Calculator import Calculator
from final_cal.ReportGenerator import ReportGenerator
from final_cal.FileManager import FileManager
import pandas as pd


# ExcelProcessor: 模板方法模式，定义处理Excel表的步骤
class ExcelProcessor:
    def __init__(self, filter_strategy: FilterStrategy, report_generator: ReportGenerator, calculator: Calculator = None):
        self.filterStrategy = filter_strategy
        self.calculator = calculator
        self.report_generator = report_generator
        self.flag = True

    def process(self, directory_paths: list, output_path: str, keyword: str, header: int):
        file_manager = FileManager(directory_paths, keyword)
        excel_files = file_manager.get_excel_files()
        all_data = pd.DataFrame()
        if self.flag:
            for file_path in excel_files:
                data = file_manager.read_excel(file_path, header=header)
                filtered_data = self.filterStrategy.filter(data, file_path=file_path, flag=True)
                all_data = pd.concat([all_data, filtered_data])
            self.flag = False
        all_data = self.filterStrategy.filter(all_data, flag=self.flag)
        if self.calculator:
            summed_data = self.calculator.calculate(all_data)
        else:
            summed_data = all_data
        self.report_generator.generate_report(summed_data, output_path)
        return summed_data


# 子类化 重写process
class TwoExcelProcess(ExcelProcessor):
    # super().__init__()

    def process(self):
        pass



