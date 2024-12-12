"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : excel_data
@File : sort_df1-df2.py
@Author : 帅张张
@Time : 2024/12/4 19:24

"""
import pandas as pd
import os
base_path = r'D:\Work_Content\新乡灾后重建安置房项目\44、工程数量台账化管理\5、结算\11、复核专门文件\0、2024.12.4改土方复核三个标段\复核所有工程量'
df1_file_name = '一标材料调差'
df2_file_name = '一标'
df1_path = base_path + '\\' + df1_file_name + '.xlsx'
df2_path = base_path + '\\' + df2_file_name + '.xlsx'

# 读取两个 Excel 文件
df1 = pd.read_excel(df1_path)  # 替换成实际文件路径
df2 = pd.read_excel(df2_path)  # 替换成实际文件路径


# 去除列名和数据中的多余空格
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

df1 = df1.apply(lambda x: x.strip() if isinstance(x, str) else x)
df2 = df2.apply(lambda x: x.strip() if isinstance(x, str) else x)

# 合并数据：内连接（匹配行）
df_matched = pd.merge(df1, df2, how='inner', left_on=['名称', '规格型号', '单位'], right_on=['名称', '规格型号', '单位'])

# 找出df1有而df2没有的行（左连接）
df1_only = pd.merge(df1, df2, how='left', left_on=['名称', '规格型号', '单位'], right_on=['名称', '规格型号', '单位'], indicator=True)
df1_only = df1_only[df1_only['_merge'] == 'left_only'].drop(columns=['_merge'])

# 找出df2有而df1没有的行（右连接）
df2_only = pd.merge(df1, df2, how='right', left_on=['名称', '规格型号', '单位'], right_on=['名称', '规格型号', '单位'], indicator=True)
df2_only = df2_only[df2_only['_merge'] == 'right_only'].drop(columns=['_merge'])

# 保存结果
df_matched.to_excel(os.path.join(base_path, f"{df1_file_name}{df2_file_name}都有.xlsx"), index=False)
df1_only.to_excel(os.path.join(base_path, f"{df1_file_name}有{df2_file_name}没有.xlsx"), index=False)
df2_only.to_excel(os.path.join(base_path, f"{df2_file_name}有{df1_file_name}没有.xlsx"), index=False)

print("文件已保存！")