import time
import threading


from scrape import scrape_trucks, get_message, get_truck_drivers, check_load_scraped
from zoom import send_sms, check_load_texted


def main():
    load_id = 137382785

    # Get info about load and truck driver phones
    if check_load_scraped(load_id):
        print(f"Info about load with id = {load_id} is already prepared")
    else:
        scrape_trucks(load_id)

    # Texting available driver from the load
    if check_load_texted(load_id):
        print(f"All drivers about load with id = {load_id} had already been informed!")
    else:
        # Load message and truck driver phones
        message = get_message(load_id)
        truck_drivers = get_truck_drivers(load_id)

        # Send message
        zoom_exe_file_path = r"C:\Users\izejd\AppData\Roaming\Zoom\bin\Zoom.exe"

        # Start a thread for the send_sms function
        proba = True
        sms_thread = threading.Thread(target=send_sms, args=(zoom_exe_file_path, truck_drivers, message, load_id, proba))
        sms_thread.start()


if __name__ == '__main__':
    main()
