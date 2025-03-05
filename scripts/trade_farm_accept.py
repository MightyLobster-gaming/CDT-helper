# details for script runner
name = "Trade farm ('sell' side)"
description = "Accepts trades from master bot."
print(name, flush=True)
print(description, flush=True)

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut

locations = ut.load_locations()

trade_notif_location = locations["trading"]["tradeInviteAccept"]["coordinates"]
trade_accept_location = locations["trading"]["tradeAccept"]["coordinates"]
trade_other_accept = locations["trading"]["tradeAcceptDetect"]["coordinates"]

trade_notif_colour = (28, 112, 186)

ut.start_timer()

while True:
    # Check for trade
    if pyautogui.pixel(trade_notif_location[0], trade_notif_location[1]) == trade_notif_colour:
        print("Trade Recieved", flush=True)
        pydirectinput.moveTo(trade_notif_location[0], trade_notif_location[1])
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)

        # Wait for menu to open
        time.sleep(2)

        # wait for bot to finish adding cars
        while pyautogui.pixel(1159,391) != (45,214,86):
            time.sleep(0.75)
        
        print("Trade Accepted", flush=True)

        # Click accept
        pydirectinput.moveTo(trade_accept_location[0], trade_accept_location[1])
        pydirectinput.moveRel(None, -1)
        pydirectinput.leftClick(duration=0.02)

        time.sleep(10)
    time.sleep(2)