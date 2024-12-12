# image_recognition.py
import cv2
import numpy as np
import pyautogui
import time


class ImageRecognition:
    has_run = False

    def __init__(self, template_path, threshold=0.8):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        self.threshold = threshold
        if self.template is None:
            raise ValueError(f"无法加载模板图像: {template_path}")

            # 检查模板的大小，并准备调整模板尺寸
        self.template_resized = None
        self.adjust_template_size()

    def adjust_template_size(self):
        """
        调整模板图像大小，使其适应较小的屏幕截图
        """
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

        # 仅在模板大于截图时调整模板大小
        if screenshot_gray.shape[0] < self.template.shape[0] or screenshot_gray.shape[1] < self.template.shape[1]:
            print("模板图像的尺寸大于目标图像，正在调整模板图像的大小")
            self.template_resized = cv2.resize(self.template, (screenshot_gray.shape[1], screenshot_gray.shape[0]))
        else:
            self.template_resized = self.template

    def find_image(self):
        # 截图并转换为灰度图像
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

        # 模板匹配
        result = cv2.matchTemplate(screenshot_gray, self.template_resized, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= self.threshold)

        # 如果找到了匹配项，返回第一个匹配位置（左上角坐标）
        if locations[0].size > 0:
            top_left_x = locations[1][0]
            top_left_y = locations[0][0]

            # 获取模板的尺寸
            template_width = self.template_resized.shape[1]
            template_height = self.template_resized.shape[0]

            # 计算匹配位置的中心坐标
            center_x = top_left_x + template_width // 2
            center_y = top_left_y + template_height // 2

            return center_x, center_y

        return None

    # def compare_screenshot(self) -> bool:
    #     pass
