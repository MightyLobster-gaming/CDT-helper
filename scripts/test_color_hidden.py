# imports
import pyautogui
import utils_hidden as ut

ut.start_timer()

print(f"Color: {pyautogui.pixel(100, 100)}", flush=True)