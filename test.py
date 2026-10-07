"""
处理两个Excel文件：
1. 从file1.xlsx的A列提取数字（格式："郑州-[3868, 4628]"）
2. 将file2.xlsx的B列对应行号的值改为file1.xlsx的C列值
"""
import pandas as pd
import openpyxl
import re
from pathlib import Path


def extract_numbers_from_a_column(value):
    """
    从A列的值中提取数字列表
    例如："郑州-[3868, 4628]" -> [3868, 4628]
    """
    if pd.isna(value):
        return []

    value_str = str(value)
    # 使用正则表达式提取方括号内的数字
    pattern = r'\[([\d\s,]+)\]'
    match = re.search(pattern, value_str)

    if match:
        # 提取数字字符串并分割
        numbers_str = match.group(1)
        # 分割并转换为整数，过滤掉无效值
        numbers = []
        for num_str in numbers_str.split(','):
            num_str = num_str.strip()
            if num_str and num_str.isdigit():
                num = int(num_str)
                if num > 0:  # 确保行号大于0
                    numbers.append(num)
        return numbers
    return []


def update_file2_from_file1(file1_path, file2_path, output_path=None):
    """
    根据file1.xlsx更新file2.xlsx

    :param file1_path: file1.xlsx的路径
    :param file2_path: file2.xlsx的路径
    :param output_path: 输出文件路径，如果为None则覆盖file2.xlsx
    """
    # 读取file1.xlsx
    print(f"正在读取 {file1_path}...")
    df1 = pd.read_excel(file1_path, engine='openpyxl')

    # 读取file2.xlsx（使用openpyxl以保持格式）
    print(f"正在读取 {file2_path}...")
    wb2 = openpyxl.load_workbook(file2_path)
    ws2 = wb2.active  # 使用活动工作表，如果需要指定工作表，可以使用 wb2['Sheet1']

    # 处理file1的每一行
    updated_count = 0
    for idx, row in df1.iterrows():
        # 获取A列的值（根据实际文件调整列索引）
        a_value = row.iloc[9]  # 第10列（J列）
        # 获取C列的值（根据实际文件调整列索引）
        c_value = row.iloc[12]  # 第13列（M列）

        # 从A列提取数字
        row_numbers = extract_numbers_from_a_column(a_value)
        
        # 调试信息
        if row_numbers:
            print(f"  行 {idx+1}: 从 '{a_value}' 提取到行号: {row_numbers}, C列值: {c_value}")

        if row_numbers and pd.notna(c_value):
            # 更新file2.xlsx的B列对应行
            for row_num in row_numbers:
                # 验证行号是否有效（必须大于0）
                if row_num < 1:
                    print(f"  警告：跳过无效行号 {row_num}（行号必须大于0）")
                    continue
                row_num += 2
                # Excel行号从1开始，所以直接使用row_num
                # B列是第2列（openpyxl中列从1开始）
                # 注意：column=2 是B列，column=11 是K列
                try:
                    cell = ws2.cell(row=row_num, column=11)
                    
                    # 检查是否是合并单元格
                    # 如果是合并单元格，需要找到合并区域的主单元格（左上角）
                    is_merged = False
                    for merged_range in ws2.merged_cells.ranges:
                        if cell.coordinate in merged_range:
                            # 找到合并区域的主单元格（左上角）
                            # openpyxl中，合并单元格的主单元格在min_row和min_col位置
                            cell = ws2.cell(row=merged_range.min_row, column=merged_range.min_col)
                            print(f"  注意：行 {row_num} 是合并单元格的一部分，将更新主单元格 {cell.coordinate}")
                            is_merged = True
                            break
                    
                    old_value = cell.value
                    cell.value = c_value
                    print(f"  更新 B{row_num} ({cell.coordinate}): {old_value} -> {c_value}")
                    updated_count += 1
                except (ValueError, AttributeError) as e:
                    print(f"  错误：无法更新行 {row_num}，列 2: {e}")
                    print(f"    行号: {row_num}, 列号: 2")
                    import traceback
                    traceback.print_exc()
                    continue

    # 保存文件
    if output_path is None:
        output_path = file2_path

    print(f"\n正在保存到 {output_path}...")
    wb2.save(output_path)
    print(f"完成！共更新了 {updated_count} 个单元格。")


if __name__ == '__main__':
    import sys
    print("=" * 50)
    print("开始执行脚本...")
    print("=" * 50)
    
    # 文件路径
    file1_path = 'file1.xlsx'
    file2_path = 'file2.xlsx'
    output_path = 'file2_updated.xlsx'  # 可以改为None来覆盖原文件

    # 检查文件是否存在
    print(f"检查文件 {file1_path}...")
    if not Path(file1_path).exists():
        print(f"错误：文件 {file1_path} 不存在！")
        sys.exit(1)
    
    print(f"检查文件 {file2_path}...")
    if not Path(file2_path).exists():
        print(f"错误：文件 {file2_path} 不存在！")
        sys.exit(1)
    
    print("文件检查通过，开始处理...\n")
    try:
        update_file2_from_file1(file1_path, file2_path, output_path)
        print("\n" + "=" * 50)
        print("脚本执行完成！")
        print("=" * 50)
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)