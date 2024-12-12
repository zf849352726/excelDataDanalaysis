# keyboard_control.py
import pyautogui
from config import Config


class KeyboardControl:
    def type(self, text):
        pyautogui.write(text, interval=Config.get_delay())

    def press_key(self, key):
        pyautogui.press(key)