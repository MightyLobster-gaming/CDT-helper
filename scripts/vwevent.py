import pyautogui
import pydirectinput
import time
import random
import utils_hidden as ut

def detect_disconnect(im):
    return False

def reconnect():
    pass

ut.start_timer()

def open_event_menu():
    loc = (33,590)
    pydirectinput.moveTo(loc[0], loc[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.5)

def check_available_kit():
    loc = (1114,709)
    screen = pyautogui.screenshot()
    if ut.get_pixel_color(loc, screen) != (100, 100, 0) and ut.get_pixel_color((1031,699), screen) != (35,35,35):
        print("Kit available", flush=True)
        pydirectinput.moveTo(loc[0], loc[1])
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)
        time.sleep(2)
        # if pyautogui.pixel(845,790) == (255,170,0):
        print("Kit opened", flush=True)
        pydirectinput.moveTo(845,790)
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)
        time.sleep(0.5)

def open_shop_menu():
    loc = (33,467)
    pydirectinput.moveTo(loc[0], loc[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.5)

try:
    counter = 0
    alternate = False
    while True:
        if counter == 20:
            counter = 0
            if alternate:
                open_event_menu()
                check_available_kit()
            else:
                open_shop_menu()
            alternate = not alternate

        counter += 1
        # im = pyautogui.screenshot()
        # if detect_disconnect(im):
        #     reconnect()
        pydirectinput.keyDown("w")
        pydirectinput.press("a")
        time.sleep(1.4+random.random()/10)
except:
    pydirectinput.keyUp("w")