import sys
import datetime
import time
import warnings
import json
import os

from pywinauto.application import Application
from pynput.keyboard import Key, Listener


# Flag to control the execution
stop_action = False


def on_press(key):
    global stop_action
    if key == Key.esc:
        stop_action = True


# Start the listener
listener = Listener(on_press=on_press)
listener.start()


# Method for opening the Zoom and sending the message
def send_sms(exe_file_path, truck_drivers, message, load_id, proba=False):
    warnings.filterwarnings("ignore", message="The window has not been focused due to")

    zoom_app = (Application(backend="uia")
                .start(exe_file_path)
                .connect(title="Zoom", timeout=100))

    global stop_action

    try:
        phone_tab = zoom_app.Zoom.child_window(title_re="Phone.*", control_type="TabItem").wrapper_object()
        phone_tab.click_input()

        sms_tab = zoom_app.Zoom.child_window(title_re="SMS.*", control_type="TabItem").wrapper_object()
        sms_tab.click_input()

        # message needs to be ready for Zoom:
        message = message.replace("\n", "+{ENTER}").replace(" ", "{SPACE}")

        first = True
        for contact in truck_drivers:
            # If user press Esc it will stop the action after sending last message
            if stop_action:
                zoom_app.kill()
                break

            if not contact["sms_sent"]:
                new_sms = zoom_app.Zoom.child_window(title="New SMS", control_type="Button",
                                                     found_index=0).wrapper_object()
                new_sms.click_input()

                send_to = zoom_app.Zoom.child_window(title_re="Send to.*", control_type="Edit",
                                                     found_index=0).wrapper_object()
                send_to.click_input()
                send_to.type_keys("^a{BACKSPACE}" + contact["phone_number"] + "{ENTER}")

                text = zoom_app.Zoom.child_window(title_re="Text.*", found_index=0).wrapper_object()
                text.click_input()

                if first:
                    time.sleep(1)

                text.type_keys("^a{BACKSPACE}" + message)

                send_message = zoom_app.Zoom.child_window(title_re="Ctrl+.*", control_type="Button",
                                                          found_index=0).wrapper_object()

                if not proba:
                    send_message.click_input()
                    contact["sms_sent"] = True
                else:
                    text.type_keys("^a{BACKSPACE}")

        # If everything went ok without problem, it will write in texted file which load id is finished
        if not stop_action:
            print(f"All drivers about load with id = {load_id} have been informed!")
            load_finished(load_id)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    finally:
        with open(f"./files/truck_infos/info_{load_id}.txt", "w") as file:
            json.dump(truck_drivers, file)

        listener.stop()

        if zoom_app.is_process_running():
            zoom_app.kill()


def write_file(zoom_app, name):
    with open(f"./files/control_identifiers{name}.txt", "w") as file:
        # Redirect standard output to the file
        sys.stdout = file
        zoom_app.Zoom.print_control_identifiers()
        # Reset standard output
        sys.stdout = sys.__stdout__


def load_finished(id):
    with open("./files/finished.txt", "a+") as file:
        file.write(f"{id}\t{datetime.datetime.now()}\n")


def check_load_texted(id):
    filename = "./files/finished.txt"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file.readlines():
                if id == int(line.split("\t")[0].strip()):
                    return True
    return False
