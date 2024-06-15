"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : final_cal
@File : FilterStrategy.py
@Author : 帅张张
@Time : 2024/6/11 10:33

"""
import pandas as pd
from final_cal.FileManager import FileManager


class FilterStrategy:
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses should implement this filter method.")


# ProjectNameFeatureFilter: 具体的筛选策略
class ProjectNameFeatureFilter(FilterStrategy):
    def __init__(self, feature: str):
        self.feature = feature

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:  # data为起始值
        filtered_data = data[data['项目名称与特征'].astype(str).str.contains(self.feature, na=False)]
        return filtered_data


class NameProjectFeatureUnitSameFilter(FilterStrategy):
    def __init__(self, conditions: list, sum_col: str):
        """
        初始化筛选器
        :param conditions: 条件列表，eg.['名称', '项目特征描述', '计量单位']
        :param sum_col: 需求和的列名，eg."工程量"
        """
        self.conditions = conditions
        self.sum_col = sum_col

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:  # data为起始值
        # 定义一个字典，指定每个列的聚合方式
        agg_dict = {col: 'first' for col in data.columns if col not in self.conditions}
        agg_dict[self.sum_col] = 'sum'

        # 对相同“名称”、“项目特征描述”、“计量单位”的行进行“工程量”列求和，保留其他列的原始数据
        aggregated_data = data.groupby(
            self.conditions, as_index=False
        ).agg(agg_dict)

        return aggregated_data


class GeneralFilter(FilterStrategy):
    def __init__(self, conditions: list[tuple[int, any]]):
        """
        初始化筛选器
        :param conditions: 条件列表，每个条件是一个元组 (第几列, 值)
        """
        self.conditions = conditions

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        根据条件列表连续筛选数据
        :param data: 要筛选的DataFrame
        :return: 筛选后的DataFrame
        """
        filtered_data = data.copy()
        columns = filtered_data.columns
        for col_num, value in self.conditions:
            filtered_data = filtered_data[filtered_data[columns[col_num]].astype(str).str.contains(value, na=False)]
        return filtered_data
