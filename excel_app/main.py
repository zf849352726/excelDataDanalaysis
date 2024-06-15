import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal
from ui import *
from moudles.ExcelProcessor import ExcelProcessor
from moudles.FilterStrategy import *
from moudles.ReportGenerator import *
from moudles.Calculator import *


class MainWindow(QMainWindow, Ui_MainWindow):
    folderPathChanged = pyqtSignal(str)  # 定义一个文件夹路径变化的信号
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.SelectNeedDataAnalysisDirButton.clicked.connect(self.openFileDialog)
        self.folderPathChanged.connect(self.handleFolderPathChanged)

    def openFileDialog(self):
        # 打开文件夹选择对话框
        folderName = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if folderName:
            print(f'Selected folder: {folderName}')
            self.SelectPathLineEdit.setText(folderName)
            self.folderPathChanged.emit(folderName)  # 发射信号，将文件夹路径发送出去

    def handleFolderPathChanged(self, folderName):
        # 调用处理文件的函数，并传递文件夹路径
        process_folder(folderName)


def process_folder(folderName):
    # 在这里编写处理文件夹的逻辑，例如打印文件夹路径
    print(f"Processing folder: {folderName}")

    # 示例使用
    directory_paths = [
        os.path.join(folderName, ''),
    ]
    output_path = os.path.join(folderName, 'out.xlsx', )
    keyword = '建筑工程'

    # filter_strategy = GeneralFilter([(4, "砖基础"), (3, "001")])
    filter_strategy = NameProjectFeatureUnitSameFilter(['项目名称与特征'], '审定')
    report_generator = SubReport()

    processor = ExcelProcessor(filter_strategy, report_generator)
    processor.process(directory_paths, output_path, keyword, 2)

    print(f"Report generated at {output_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
