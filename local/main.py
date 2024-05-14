import time
import threading
import os

from scrape import scrape_trucks, get_message, get_truck_drivers, check_load_scraped
from zoom import send_sms, check_load_texted
from pynput.keyboard import Key, Listener
from listener import stop_action


def on_press(key):
    if key == Key.esc:
        print(key)
        stop_action[0] = True


def main(load_id, proba=False):
    # Get info about load and truck driver phones
    if check_load_scraped(load_id):
        print(f"Info about load with id = {load_id} is already prepared")
    else:
        scrape_trucks(load_id)

    if stop_action[0]:
        return

    # Texting available driver from the load
    if check_load_texted(load_id):
        print(f"All drivers about load with id = {load_id} had already been informed!")
    else:
        # Load message and truck driver phones
        message = get_message(load_id)
        truck_drivers = get_truck_drivers(load_id)

        sent = len(list(filter(lambda d: d["sms_sent"], truck_drivers)))
        print(f"{sent}/{len(truck_drivers)} drivers informed about load with id = {load_id}... \n")

        # Send message
        zoom_exe_file_path = r"C:\Users\izejd\AppData\Roaming\Zoom\bin\Zoom.exe"

        # Start a thread for the send_sms function
        sms_thread = threading.Thread(target=send_sms, args=(zoom_exe_file_path, truck_drivers, message, load_id, proba))
        sms_thread.start()

        sms_thread.join()


if __name__ == '__main__':
    # Start listener - if esc is pressed
    listener = Listener(on_press=on_press)
    listener.start()

    for load_id in [137927582]:
        if stop_action[0]:
            break
        
        main(load_id)

    listener.stop()

