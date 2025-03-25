# details for script runner
name = "Cross-trade spam (buy-side)"
description = "Buys from stall and trades back"
print(description, flush=True)

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut
from PIL import Image
import pytesseract


locations = ut.load_locations()

shop_menu_location = locations["shop"]["shopMenuOutCar"]["coordinates"]
shop_search_location = locations["shop"]["shopSearch"]["coordinates"]
buy_button = locations["shop"]["shopRegularBuy"]["coordinates"]
robux_buy_button = locations["shop"]["shopRobuxBuy"]["coordinates"]

trade_menu_location = locations["trading"]["tradeMenuTradingServer"]["coordinates"]
trade_invite_location = locations["trading"]["tradeInviteAccept"]["coordinates"]
trade_search_location = locations["trading"]["tradeCarSearch"]["coordinates"]

trade_car_location = locations["trading"]["tradeFirstCar"]["coordinates"]

trade_accept_location = locations["trading"]["tradeAccept"]["coordinates"]
trade_complete_close = locations["trading"]["tradeCompleteClose"]["coordinates"]

stall_first_car = locations["trading"]["stallCarPos"]["coordinates"]
stall_accept = locations["trading"]["stallBuyConfirm"]["coordinates"]
stall_close = locations["trading"]["stallClose"]["coordinates"]

def read_image(img):
    # Extract text using Tesseract OCR
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

def wait_for_car():

    car_available = False
    while not car_available:
        # open menu
        pydirectinput.press("e")
        time.sleep(0.9)
        if ut.get_pixel_color(stall_first_car) == (0,0,0):
            car_available = True
        else:
            # close menu
            pydirectinput.moveTo(stall_close[0], stall_close[1])
            pydirectinput.moveRel(None, -1)
            pydirectinput.leftClick(duration=0.02)
            time.sleep(0.3)
    # buy car
    pydirectinput.moveTo(stall_first_car[0], stall_first_car[1]+20)
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    # confirm
    pydirectinput.moveTo(stall_accept[0], stall_accept[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.8)

def open_trade_menu():
    # Select trade location from the side
    pydirectinput.moveTo(trade_menu_location[0], trade_menu_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.5)

def trade(trade_account, car):

    # When trade search eventually works
    # pydirectinput.moveTo(trade_search_location[0], trade_search_location[1])
    # pydirectinput.moveRel(None, -1)
    # pydirectinput.leftClick(duration=0.02)
    # for character in trade_account:
    #     pydirectinput.press(character, _pause=False)

    # # Invite top player
    # pydirectinput.moveTo(trade_invite_location[0], trade_invite_location[1])
    # pydirectinput.moveRel(None, -1)
    # pydirectinput.leftClick(duration=0.02)
    # print("Trade Invite sent", flush=True)

    # Wait until in trade
    while ut.get_pixel_color(trade_accept_location) != (30,162,63):
        time.sleep(1)
    print("Trade Invite accepted", flush=True)

    # Search for car
    pydirectinput.moveTo(trade_search_location[0], trade_search_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.05)
    for character in car:
        pydirectinput.press(character, _pause=False)

    # Select car
    pydirectinput.moveTo(trade_car_location[0], trade_car_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

    time.sleep(0.05)
    # Accept trade
    pydirectinput.moveTo(trade_accept_location[0], trade_accept_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    print("Trade Accepted", flush=True)
    time.sleep(5)
    wait_for_trade_complete()

def wait_for_trade_complete():
    while ut.get_pixel_color(trade_complete_close[0], trade_complete_close[1]) != (208,0,3):
        time.sleep(0.5)

def find_trade_player(target_name):
    pydirectinput.moveTo(trade_invite_location[0], trade_invite_location[1])
    pydirectinput.moveRel(None, -1)
    for scroll in range(20):
        pyautogui.scroll(1000)
    found = False
    previous_pics = []
    while not found:
        img = pyautogui.screenshot()
        startend_pixels = []
        for pixel in range(420, 715):
            if ((startend_pixels and len(startend_pixels[-1]) == 2) or not startend_pixels) and ut.get_pixel_color((1025, pixel), img=img) == (73,75,72):
                startend_pixels.append([pixel])
            elif (startend_pixels and len(startend_pixels[-1]) == 1) and ut.get_pixel_color((1025, pixel), img=img) == (39,39,39):
                startend_pixels[-1].append(pixel)
        for bounds in startend_pixels:
            if len(bounds) == 2 and bounds[1]-bounds[0] > 68 and bounds[1]-bounds[0] < 72:
                copy = img
                copy = copy.crop((785, bounds[0], 1025, bounds[0]+40))
                # copy.save(f"test{bounds}.png")
                if copy not in previous_pics:
                    previous_pics.append(copy)
                    text = read_image(copy).replace("\n", "")
                    if text==target_name:
                        found = bounds
                        break
        if not found:
            pyautogui.scroll(-1000)
            time.sleep(0.1)

    # invite player
    pydirectinput.moveTo(trade_invite_location[0], int(found[0] + (found[1]-found[0])/2))
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

ut.start_timer()

target_name="MightyLobsterAlt"

wait_for_car()
open_trade_menu()
find_trade_player(target_name)
trade(trade_account="", car="")
