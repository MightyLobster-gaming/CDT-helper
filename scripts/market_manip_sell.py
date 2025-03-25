# details for script runner
name = "Cross-trade spam (sell-side)"
description = "Puts car for sale and trades back tokens"
print(description, flush=True)

# imports
import pyautogui
import pydirectinput
import time
import utils_hidden as ut

locations = ut.load_locations()

trade_notif_location = locations["trading"]["tradeInviteAccept"]["coordinates"]
trade_accept_location = locations["trading"]["tradeAccept"]["coordinates"]
trade_token_box = locations["trading"]["tradeTokenBox"]["coordinates"]
trade_other_accept = locations["trading"]["tradeAcceptDetect"]["coordinates"]

stall_config_inv_car_pos = locations["trading"]["stallConfigInvPos"]["coordinates"]
stall_config_car_pos = locations["trading"]["stallConfigCarPos"]["coordinates"]
stall_config_close = locations["trading"]["stallConfigClose"]["coordinates"]

stall_enter_tokens = locations["trading"]["stallEnterTokens"]["coordinates"]
stall_confirm_tokens = locations["trading"]["stallConfirmTokens"]["coordinates"]

trade_complete_close = locations["trading"]["tradeCompleteClose"]["coordinates"]

trade_notif_colour = (28, 112, 186)

def check_if_sold():
    # open config
    pydirectinput.press("e")
    time.sleep(0.5)
    output = ut.get_pixel_color(stall_config_car_pos) != (0,0,0)
    # close config
    pydirectinput.moveTo(stall_config_close[0], stall_config_close[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    return output
    
def list_car_for_sale(token_amount):
    # open config
    pydirectinput.press("e")
    time.sleep(0.5)
    # select car
    pydirectinput.moveTo(stall_config_inv_car_pos[0], stall_config_inv_car_pos[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    # enter token amount
    pydirectinput.moveTo(stall_enter_tokens[0], stall_enter_tokens[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)
    for character in str(token_amount):
        pydirectinput.press(character)
    # confirm
    pydirectinput.moveTo(stall_confirm_tokens[0], stall_confirm_tokens[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

def wait_for_trade():
    trade = False
    while not trade:
        if pyautogui.pixel(trade_notif_location[0], trade_notif_location[1]) == trade_notif_colour:
            trade = True
        else:
            time.sleep(0.5)

    print("Trade Recieved", flush=True)
    pydirectinput.moveTo(trade_notif_location[0], trade_notif_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

    # Wait for menu to open
    time.sleep(2)

def trade(token_amount):
    # select token box
    pydirectinput.moveTo(trade_token_box[0], trade_token_box[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

    # enter tokens
    for character in str(token_amount):
        pydirectinput.press(character)

    # wait for bot to finish adding cars
    while pyautogui.pixel(1159,391) != (45,214,86):
        time.sleep(0.75)
    
    print("Trade Accepted", flush=True)

    # Click accept
    pydirectinput.moveTo(trade_accept_location[0], trade_accept_location[1])
    pydirectinput.moveRel(None, -1)
    pydirectinput.leftClick(duration=0.02)

    time.sleep(5)
    wait_for_trade_complete()

def wait_for_trade_complete():
    while ut.get_pixel_color(trade_complete_close[0], trade_complete_close[1]) != (208,0,3):
        time.sleep(0.5)