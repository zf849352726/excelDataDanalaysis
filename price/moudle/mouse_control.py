# mouse_control.py
from config import Config
import pydirectinput as pdi
import time

class MouseControl:
    def __init__(self):
        self.position = (0, 0)
        self.distance = 0
        pdi.FAILSAFE = True  # 让鼠标移到屏幕角落可以终止任务

    def move_to(self, x, y):
        self.position = (x, y)
        # 鼠标移动
        pdi.moveTo(x, y, duration=Config.get_delay())

    def click(self):
        try:
            pdi.click()
        except Exception as e:
            print(e)

    def scroll(self, distance):
        self.distance = distance
        pdi.scroll(distance)
