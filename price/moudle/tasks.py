# tasks.py
from config import Config
from pathlib import Path
from automator import Automator
from pathlib import Path

def run_task(c_task_name):
    automator = Automator()
    automator.execute_task(c_task_name)


def task(c_task_img_path):
    print(c_task_img_path)
    export_excel_task_path = Path(BASE_PATH) / c_task_img_path

    # 获取目录下所有文件的文件名（只取文件）
    export_excel_task_imgs_file_names = [f for f in export_excel_task_path.iterdir() if f.is_file()]
    # print([f.name for f in export_excel_task_imgs_file_names])

    # 根据序号顺序执行任务
    for img in sorted(export_excel_task_imgs_file_names, key=lambda x: x.stem):  # 按文件名排序
        Automator.task_img_path = Path(img.resolve())
        task_name = img.stem.split('-')[-1]  # 只取文件名，不含扩展名
        # print(task_name)
        try:
            run_task(task_name)
        except Exception as e:
            print(f"任务 {task_name} 执行失败: {e}")


if __name__ == "__main__":
    # 获取任务路径
    BASE_PATH = Config.get_img_base_path()

    # 功能1 批量导excel-清单带子目
    task('export_excel_task')

    # 功能2 一个单位工程整个项目临时删除
    task('temporary_deletion_task')


