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
from pathlib import Path

class FilterStrategy:
    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:
        raise NotImplementedError("Subclasses should implement this filter method.")


# ProjectNameFeatureFilter: 具体的筛选策略
class ProjectNameFeatureFilter(FilterStrategy):
    def __init__(self, feature: str):
        self.feature = feature

    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:  # data为起始值
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

    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:  # data为起始值
        try:
            file_name = Path(file_path).parent.name
            # 处理缺失值
            data = data.fillna({col: 'Unknown' for col in self.conditions})
            data[self.sum_col] = pd.to_numeric(data[self.sum_col], errors='coerce')
            if flag:
                # 定义一个字典，指定每个列的聚合方式
                agg_dict = {col: every_col_agg_method for col in data.columns if col not in self.conditions}
                # 对 `sum_col` 使用自定义拼接
                agg_dict[self.sum_col] = 'sum'
                aggregated_data = data.groupby(
                    self.conditions, as_index=False
                ).agg(agg_dict)
                # 获取每组的原始索引列表，并格式化为 'file1-0,3,6' 这样的字符串
                indexes = data.groupby(self.conditions).apply(
                    lambda group: f"{file_name}-{str(group.index.tolist())}").reset_index(name='数据源')

                # 合并求和结果和索引信息
                result = pd.merge(aggregated_data, indexes, on=self.conditions)
                # print(result)

                return result
            else:
                # 定义一个字典，指定每个列的聚合方式
                self_conditions = self.conditions.copy()
                self_conditions.append('数据源')
                agg_dict = {col: every_col_agg_method for col in data.columns if col not in self_conditions}
                # 对 `sum_col` 使用自定义拼接
                agg_dict[self.sum_col] = 'sum'
                agg_dict['数据源'] = lambda x: '+'.join(str(val) for val in x if pd.notna(val))

                aggregated_data = data.groupby(
                    self.conditions, as_index=False
                ).agg(agg_dict)

                return aggregated_data
        except Exception as e:
            print(e)


class NameProjectFeatureUnitSameFilterList(FilterStrategy):
    def __init__(self, conditions: list, sum_col: str):
        """
        初始化筛选器
        :param conditions: 条件列表，eg.['名称', '项目特征描述', '计量单位']
        :param sum_col: 需求和的列名，eg."工程量"
        """
        self.conditions = conditions
        self.sum_col = sum_col

    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:  # data为起始值
        try:
            file_name = Path(file_path).parent.name
            # 处理缺失值
            data = data.fillna({col: 'Unknown' for col in self.conditions})
            data[self.sum_col] = pd.to_numeric(data[self.sum_col], errors='coerce')
            if flag:
                # 定义一个字典，指定每个列的聚合方式
                agg_dict = {col: every_col_agg_method for col in data.columns if col not in self.conditions}
                # 对 `sum_col` 使用自定义拼接
                agg_dict[self.sum_col] = lambda x: '+'.join(str(val) for val in x if pd.notna(val))
                aggregated_data = data.groupby(
                    self.conditions, as_index=False
                ).agg(agg_dict)
                # 获取每组的原始索引列表，并格式化为 'file1-0,3,6' 这样的字符串
                indexes = data.groupby(self.conditions).apply(
                    lambda group: f"{file_name}-{str(group.index.tolist())}").reset_index(name='数据源')

                # 合并求和结果和索引信息
                result = pd.merge(aggregated_data, indexes, on=self.conditions)
                # print(result)

                return result
            else:
                # 定义一个字典，指定每个列的聚合方式
                self_conditions = self.conditions.copy()
                self_conditions.append('数据源')
                agg_dict = {col: every_col_agg_method for col in data.columns if col not in self_conditions}
                # 对 `sum_col` 使用自定义拼接
                agg_dict[self.sum_col] = lambda x: '+'.join(str(val) for val in x if pd.notna(val))
                agg_dict['数据源'] = lambda x: '+'.join(str(val) for val in x if pd.notna(val))

                aggregated_data = data.groupby(
                    self.conditions, as_index=False
                ).agg(agg_dict)

                return aggregated_data
        except Exception as e:
            print(e)


class GeneralFilter(FilterStrategy):
    def __init__(self, conditions: list[tuple[int, any]]):
        """
        初始化筛选器
        :param conditions: 条件列表，每个条件是一个元组 (第几列, 值)
        """
        self.conditions = conditions

    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:
        """
        根据条件列表连续筛选数据
        :param flag:
        :param file_path:
        :param data_source:
        :param every_col_agg_method:
        :param data: 要筛选的DataFrame
        :return: 筛选后的DataFrame
        """
        filtered_data = data.copy()
        columns = filtered_data.columns
        for col_num, value in self.conditions:
            filtered_data = filtered_data[filtered_data[columns[col_num]].astype(str).str.contains(value, na=False)]
        return filtered_data


class CompareTwoExcel(FilterStrategy):
    def __init__(self, conditions: list):
        """
        对比列名列表
        :param conditions: 条件列表，eg.['名称', '项目特征描述', '计量单位']
        :param sum_col: 需求和的列名，eg."工程量"
        """
        self.conditions = conditions

    def filter(self, data: pd.DataFrame, every_col_agg_method: str = 'first', file_path: str = '', flag: bool = True) -> pd.DataFrame:  # data为起始值
        # 处理缺失值
        data = data.fillna({col: 'Unknown' for col in self.conditions})

        # 确保要进行求和的列是数值类型
        data[self.sum_col] = pd.to_numeric(data[self.sum_col], errors='coerce')

        # 确保要进行求和的列是数值类型
        data[self.sum_col] = pd.to_numeric(data[self.sum_col], errors='coerce')

        # 定义一个字典，指定每个列的聚合方式
        agg_dict = {col: 'first' for col in data.columns if col not in self.conditions}
        agg_dict[self.sum_col] = 'sum'

        # 对相同“名称”、“项目特征描述”、“计量单位”的行进行“工程量”列求和，保留其他列的原始数据
        aggregated_data = data.groupby(
            self.conditions, as_index=False
        ).agg(agg_dict)

        return aggregated_data
