# automator.py
from price.moudle.image_recognition import ImageRecognition
from price.moudle.mouse_control import MouseControl
from price.moudle.keyboard_control import KeyboardControl
import time


class Automator:
    task_img_path = ''

    def __init__(self, tm):
        self.task_name = ''
        self.mouse_control = MouseControl()
        self.keyboard_control = KeyboardControl()
        self.tm = tm

    def execute_task(self, task_name):
        # 根据任务名调用不同的任务方法
        self.task_name = task_name
        if 'click' in task_name:
            self._click_button_task()
        if 'cknoreg' in task_name:
            x = int(task_name.split('_')[-1])
            y = int(task_name.split('_')[-2])
            self._click_button_no_reg(x, y)
        if 'sleep' in task_name:
            time_num = int(task_name.split('_')[-1]) 
            self._sleep(time_num)
        if 'mouse_scroll' in task_name:
            scroll_distance = int(task_name.split('_')[-1])
            self._mouse_scroll_task(scroll_distance)
        if 'press' in task_name:
            press_list = task_name.split('_')[1:]
            self._press_key(press_list)

        if 'text' in task_name:
            text = task_name.split('_')[-1]
            self._type_text_task(text)

    def _click_button_task(self):
        print(f"开始点击按钮任务...{self.task_name}")
        img_recog = ImageRecognition(Automator.task_img_path, tm=self.tm, threshold=0.8)
        # print(self.task_name)
        # print(Automator.task_img_path)

        position = img_recog.find_image()
        if position:
            # time.sleep(0.5)
            # 关键代码 控制执行
            self.mouse_control.move_to(position[0], position[1])
            self.mouse_control.click()
        else:
            print("按钮未找到！")

    def _click_button_no_reg(self, x, y):
        print(f"开始点击按钮任务...{self.task_name}")
        position = (x, y)
        self.mouse_control.click(position)

    def _type_text_task(self, text):
        print(f"开始输入任务：{text}")
        self.keyboard_control.type(text)

    def _mouse_scroll_task(self, distance):
        print(f"鼠标滚动距离：{distance}")
        self.mouse_control.scroll(distance)

    def _sleep(self, time_num):
        time.sleep(time_num)

    def _press_key(self, key):
        self.keyboard_control.press_key(key)
