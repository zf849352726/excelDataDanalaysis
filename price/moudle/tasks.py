from PyQt5.QtCore import QThread, pyqtSignal

from config import Config


class FunctionThread(QThread):
    # # task_signal = pyqtSignal(str)  # 用于通知主线程执行任务
    # stop_signal = pyqtSignal()  # 停止信号

    def __init__(self, myWin):
        super().__init__()
        self.myWin = myWin  # 传入主窗口实例
        self._running = True  # 任务运行状态
        self.base_path = Config.get_img_base_path()

    # def run(self):
    #     """线程启动后，通知主线程开始任务"""
    #     self.stop_signal.connect(self.stop)  # 连接停止信号

    def stop(self):
        """停止任务"""
        self._running = False
        print("任务已停止")

    def change_state(self):
        """改变状态"""
        if self._running:
            self._running = False
        else:
            self._running = True
