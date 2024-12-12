"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : final_cal
@File : Calculator.py
@Author : 帅张张
@Time : 2024/6/11 10:33

"""
import pandas as pd


# SumCalculator: 负责对筛选后的数据进行求和
class Calculator:
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses should implement this calculate method.")


# SumCalculator: 负责对筛选后的数据进行求和
class SumCalculator(Calculator):
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        column_sum = data.iloc[7:, 8].sum()
        # 保留前四行并删除其他行
        selected_data = data.iloc[:4]
        selected_data.iat[0, 9] = column_sum

        return selected_data


