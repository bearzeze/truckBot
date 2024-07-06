import time
import warnings
import os
import django
import pyperclip
import sys

from django.core.cache import cache
from django.contrib import messages

from pywinauto.application import Application

from .models import Load, Driver, LoadHistory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

# Method for opening the Zoom and sending the message
def send_sms(request, load_ids, proba=False, palci=False):
    
    exe_file_path = request.session["zoom_exe_path"]
    
    warnings.filterwarnings("ignore", message="The window has not been focused due to")

    # Zoom version 6.1.0
    zoom_app = Application(backend="uia").start(exe_file_path).connect(title_re=r".*Zoom.*", timeout=100)
    
    zoom_window = zoom_app.window(title_re=r".*Zoom.*")
    
    time.sleep(3)
    
    last_id = load_ids[-1]
    
    for load_id in load_ids:
        
        if cache.get("stop_action"):
            stop_action(zoom_app, request)
            return
    
        load = Load.objects.get(id=load_id)
        truck_drivers = load.drivers.all()
                
        messages_zoom = creating_message_versions(request, load)
        
        try:
           
            phone_tab = zoom_window.child_window(title_re="Phone.*", control_type="TabItem").wrapper_object()
            phone_tab.click_input()

            sms_tab = zoom_window.child_window(title_re="SMS.*", control_type="TabItem").wrapper_object()
            sms_tab.click_input()
            
            # message needs to be ready for Zoom application if type_keys is hit:
            if palci:
                messages_zoom = [message.replace("\n", "+{ENTER}").replace(" ", "{SPACE}") for message in messages_zoom] 

            for idx, driver in enumerate(truck_drivers):
                # If user press Esc it will stop the action after sending last message
                if cache.get("stop_action"):
                    stop_action(zoom_app, request)
                    return

                if not driver.sms_sent:
                    result = sending_zoom_messages(zoom_window, driver, idx, messages_zoom, proba, palci)
                    
                    if result == "stop":
                        stop_action(zoom_app, request)
                        return
                        
            # If everything went ok without stopping action
            if not cache.get("stop_action"): # and not proba:
                # Load is finished, but not deleted from database
                load.finished = True
                load.save()
                # Load history object is also created
                LoadHistory.objects.create(load_id=load_id,
                                          user=request.user,
                                          drivers_informed_count=len(truck_drivers))
                # Every truck_drivers for this load is deleted from db
                truck_drivers.delete()
                
                messages.success(request, f"All drivers about load with id = {load_id} have been informed!")

        except Exception as e:
            messages.error(request, f'Error with load id {load_id} -> "{e}"')
            zoom_app.kill()
            return

        finally:
            if zoom_app.is_process_running() and last_id == load_id:
                zoom_app.kill()
                return


def sending_zoom_messages(zoom_window, driver, idx, messages_zoom, proba, palci):
    new_sms = zoom_window.child_window(title="New SMS", control_type="Button",
                                            found_index=0).wrapper_object()
    new_sms.click_input()

    send_to = zoom_window.child_window(title_re="Send to.*", control_type="Edit",
                                        found_index=0).wrapper_object()
    send_to.click_input()
    
    send_to.type_keys("^a{BACKSPACE}")
    
    if palci:
        send_to.type_keys(driver.phone_number)
    else:
        pyperclip.copy(driver.phone_number)
        send_to.type_keys("^v")
        
    send_to.type_keys("{ENTER}")

    text = zoom_window.child_window(title_re="Text.*", found_index=0).wrapper_object()
    text.click_input()

    # First iteration
    if idx == 0:
        time.sleep(1)
    
    text.type_keys("^a{BACKSPACE}")
    
    if palci:
        text.type_keys(messages_zoom[idx % len(messages_zoom)])
    else:
        pyperclip.copy(messages_zoom[idx % len(messages_zoom)])
        text.type_keys("^v")

    send_message = zoom_window.child_window(title_re="Ctrl+.*", control_type="Button",
                                            found_index=0).wrapper_object()
    
    if cache.get("stop_action"):
        return "stop"

    if not proba:
        send_message.click_input()
        driver.sms_sent = True
        driver.save()
        time.sleep(0.5)
    else:
        text.type_keys("^a{BACKSPACE}")


def stop_action(zoom_app, request):
    zoom_app.kill()
    messages.warning(request, f"You stopped sending messages!")            
    
    
def creating_message_versions(request, load):
    message1 = load.message + request.user.landstar_info1()
    message2 = load.message + request.user.landstar_info2()
    message3 = request.user.load_offer_str() + message1 
    message4 = request.user.load_offer_str() + message2

    return [message1, message2, message3, message4]


def write_control_identifiers_file(zoom_window, name):
    with open(f"./control_identifiers_{name}.txt", "w") as file:
        print("UŠOO")
        # Redirect standard output to the file
        sys.stdout = file
        zoom_window.print_control_identifiers()
        # Reset standard output
        sys.stdout = sys.__stdout__
        print("IZAŠOO")
        time.sleep(5)
