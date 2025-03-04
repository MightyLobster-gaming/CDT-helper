# details for script runner
name = "AFK Sleigh"
description = ""

# on start
print(name)
print(description)
print()

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut

ut.start_timer()

# script
pydirectinput.press("w")
try:
    counter = 0
    while True:
        if counter == 20:
            counter = 0
            pydirectinput.click()
        counter += 1
        pydirectinput.keyDown("w")
        pydirectinput.press("a")
        time.sleep(1.4)
except:
    pydirectinput.keyUp("w")