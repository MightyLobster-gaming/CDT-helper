# details for script runner
name = "Trade farm (buy side)"
description = "Buys and trades a shop car with the top account in the server."
print(name, flush=True)
print(description, flush=True)

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut

# define car to trade
car = "f5"

# trade_account = "MightyLobsterAlt"

locations = ut.load_locations()

shop_menu_location = locations["shop"]["shopMenu"]
shop_search_location = locations["shop"]["shopSearch"]
buy_button = locations["shop"]["shopRegularBuy"]
robux_buy_button = locations["shop"]["shopRobuxBuy"]

trade_menu_location = locations["trading"]["tradeMenu"]
trade_invite_location = locations["trading"]["tradeInviteAccept"]
trade_search_location = locations["trading"]["tradeCarSearch"]

trade_car_location = locations["trading"]["tradeFirstCar"]

trade_accept_location = locations["trading"]["tradeAccept"]

def open_shop():
    # Select shop location from the side
    pydirectinput.moveTo(shop_menu_location[0], shop_menu_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.5)
    # Select car tab
    # pydirectinput.moveTo(536,322)
    # pydirectinput.moveRel(None, -1)
    # pydirectinput.leftClick(duration=0.02)

def search_car(car):
    # Click on search bar
    pydirectinput.moveTo(shop_search_location[0], shop_search_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    time.sleep(0.05)
    # Type in car name
    for character in car:
        pydirectinput.press(character, _pause=False)

    # # Check if car exists
    # if pyautogui.pixel(579,417) == (10,253,2):
    #     print(f"{car}: Not found in shop")
    #     return False
    return

def buy_car(location):

    pydirectinput.moveTo(location[0], location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

    time.sleep(0.05)

    # Check for robux
    if pyautogui.pixel(1131,717) == (24,162,0):
        # Click buy button
        pydirectinput.moveTo(robux_buy_button[0], robux_buy_button[1])
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)
    else:
        # Click buy button
        pydirectinput.moveTo(buy_button[0], buy_button[1])
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)
    print("Car bought", flush=True)
    time.sleep(0.5)

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
    while pyautogui.pixel(trade_accept_location[0], trade_accept_location[1]) != (30,162,63):
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
    

ut.start_timer()

for amount in range(3):
    open_shop()
    #search_car(car)
    buy_car((712,466))
    open_trade_menu()
    trade("", car)
