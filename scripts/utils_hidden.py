import time
import json
import pyautogui

def start_timer(countdown_seconds=3):
    for n in range(countdown_seconds):
        print(f"Starting in {countdown_seconds-n}", flush=True)
        time.sleep(1)

def format_time(seconds: float) -> str:
    if seconds < 60:
        return f"{int(round(seconds))} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(round(minutes))} minutes {int(round(remaining_seconds))} seconds" if remaining_seconds else f"{int(round(minutes))} minutes"
    elif seconds < 86400:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{int(round(hours))} hours {int(round(remaining_minutes))} minutes" if remaining_minutes else f"{int(round(hours))} hours"
    else:
        days = seconds // 86400
        remaining_hours = (seconds % 86400) // 3600
        return f"{int(round(days))} days {int(round(remaining_hours))} hours" if remaining_hours else f"{int(round(days))} days"

def get_pixel_color(xytuple, img=None):
    if img:
        colour = img.getpixel(xytuple)
    else:
        colour = pyautogui.pixel(xytuple[0], xytuple[1])
    print(f"Color: {colour}", flush=True)
    return colour

def load_locations():
    with open("scripts/locations.json", "r") as f:
        locations = json.load(f)
    return locations