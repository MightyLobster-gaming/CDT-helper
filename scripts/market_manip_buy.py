# details for script runner
name = "Cross-trade spam (buy-side)"
description = "Buys from stall and trades back"
print(description, flush=True)

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut


locations = ut.load_locations()

shop_menu_location = locations["shop"]["shopMenuOutCar"]["coordinates"]
shop_search_location = locations["shop"]["shopSearch"]["coordinates"]
buy_button = locations["shop"]["shopRegularBuy"]["coordinates"]
robux_buy_button = locations["shop"]["shopRobuxBuy"]["coordinates"]

trade_menu_location = locations["trading"]["tradeMenuInGame"]["coordinates"]
trade_invite_location = locations["trading"]["tradeInviteAccept"]["coordinates"]
trade_search_location = locations["trading"]["tradeCarSearch"]["coordinates"]

trade_car_location = locations["trading"]["tradeFirstCar"]["coordinates"]

trade_accept_location = locations["trading"]["tradeAccept"]["coordinates"]

def buy_from_stall():
    pass

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

    # Invite top player
    pydirectinput.moveTo(trade_invite_location[0], trade_invite_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    print("Trade Invite sent", flush=True)

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
    time.sleep(7)