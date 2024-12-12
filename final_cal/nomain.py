from main import *

if __name__ == '__main__':
    # 示例使用
    directory_paths = [
        r'H:\py_work\final_cal\data\辉县市灾后重建项目城南片区安置区建设项目(BD地块）-审定版3标段（审核）',
    ]
    output_path = r'H:\py_work\final_cal\data\辉县市灾后重建项目城南片区安置区建设项目(BD地块）-审定版3标段（审核）\out.xlsx'
    keyword = '建筑工程'

    # filter_strategy = GeneralFilter([(4, "砖基础"), (3, "001")])
    filter_strategy = NameProjectFeatureUnitSameFilter(['项目名称与特征'], '审定')
    report_generator = SubReport()

    processor = ExcelProcessor(filter_strategy, report_generator)
    processor.process(directory_paths, output_path, keyword, 2)

    print(f"Report generated at {output_path}")