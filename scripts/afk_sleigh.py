# details for script runner
name = "AFK Sleigh"
description = "Uses either Macchina Sled or Doge Sled to automate driving, gaining you miles and money whilst afk.\nStart in your car with flying mode on. Place mouse over shop icon to prevent earnings timeout"

# on start
print(name)
print(description)
print()

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut
import json


with open("scripts/locations.json", "r") as f:
    locations = json.load(f)

shop_menu_location = locations["shop"]["shopMenu"]


ut.start_timer()

# script
pydirectinput.press("w")
try:
    counter = 0
    while True:
        if counter == 30:
            pydirectinput.moveTo(shop_menu_location[0], shop_menu_location[1])
            pydirectinput.moveRel(None, -1)
            pydirectinput.click()
            pydirectinput.press("w")
            counter = 0
        
        pydirectinput.keyDown("w")
        pydirectinput.press("a")
        time.sleep(1)
        counter += 1
except:
    pydirectinput.keyUp("w")