import sys
import datetime
import time
import warnings
import json
import os
import django

from django.core.cache import cache
from django.contrib import messages

from pywinauto.application import Application

from .models import Load, Driver, LogHistory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()


# Method for opening the Zoom and sending the message
def send_sms(request, load_id, proba=False):
    
    exe_file_path = request.session["zoom_exe_path"]
    load = Load.objects.get(id=load_id)
    truck_drivers = load.drivers.all()
    
    message = load.message + request.user.landstar_info()
    
    warnings.filterwarnings("ignore", message="The window has not been focused due to")

    zoom_app = (Application(backend="uia")
                .start(exe_file_path)
                .connect(title="Zoom", timeout=100))

    try:
        phone_tab = zoom_app.Zoom.child_window(title_re="Phone.*", control_type="TabItem").wrapper_object()
        phone_tab.click_input()

        sms_tab = zoom_app.Zoom.child_window(title_re="SMS.*", control_type="TabItem").wrapper_object()
        sms_tab.click_input()
        
        # message needs to be ready for Zoom application:
        message = message.replace("\n", "+{ENTER}").replace(" ", "{SPACE}")

        first = True
        for driver in truck_drivers:
            # If user press Esc it will stop the action after sending last message
            if cache.get("stop_action"):
                zoom_app.kill()
                break

            if not driver.sms_sent:
                new_sms = zoom_app.Zoom.child_window(title="New SMS", control_type="Button",
                                                     found_index=0).wrapper_object()
                new_sms.click_input()

                send_to = zoom_app.Zoom.child_window(title_re="Send to.*", control_type="Edit",
                                                     found_index=0).wrapper_object()
                send_to.click_input()
                send_to.type_keys("^a{BACKSPACE}" + driver.phone_number + "{ENTER}")

                text = zoom_app.Zoom.child_window(title_re="Text.*", found_index=0).wrapper_object()
                text.click_input()

                if first:
                    time.sleep(1)
                
                if cache.get("stop_action"):
                    zoom_app.kill()
                    break

                text.type_keys("^a{BACKSPACE}" + message)

                send_message = zoom_app.Zoom.child_window(title_re="Ctrl+.*", control_type="Button",
                                                          found_index=0).wrapper_object()
                
                if cache.get("stop_action"):
                    zoom_app.kill()
                    break
            
                if not proba:
                    send_message.click_input()
                    driver.sms_sent = True
                    driver.save()
                else:
                    text.type_keys("^a{BACKSPACE}")
                    
                    
        # If everything went ok without stopping action
        if not cache.get("stop_action"):
            # Load is finished, but not deleted
            load.finished = True
            load.save()
            # Log history object is also created
            LogHistory.objects.create(load_id=load_id, drivers_informed_count=len(truck_drivers))
            # Every truck_drivers for this load is deleted from db
            truck_drivers.delete()
            messages.success(request, f"All drivers about load with id = {load_id} have been informed!")
        else:
            messages.warning(request, f"You stopped sending messages!")


    except Exception as e:
        messages.error(request, f'Error with load id {load_id} -> "{e}"')

    finally:
        if zoom_app.is_process_running():
            zoom_app.kill()

