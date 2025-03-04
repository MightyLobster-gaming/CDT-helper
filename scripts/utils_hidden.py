import time


def start_timer(countdown_seconds=3):
    for n in range(countdown_seconds):
        print(f"Starting in {countdown_seconds-n}", flush=True)
        time.sleep(1)