import sys
class Config:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    OPERATION_DELAY = 0.5  # 延迟时间（秒）
    TASKS_IMG_BASE_PATH = r'D:\python_learn\excel_data\price\static'

    @staticmethod
    def get_screen_resolution():
        return Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT

    @staticmethod
    def get_delay():
        return Config.OPERATION_DELAY

    @staticmethod
    def get_img_base_path():
        return Config.TASKS_IMG_BASE_PATH
