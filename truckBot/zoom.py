import time
import warnings
import os
import django
import pyperclip

from django.core.cache import cache
from django.contrib import messages

from pywinauto.application import Application

from .models import Load, Driver, LogHistory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

# Method for opening the Zoom and sending the message
def send_sms(request, load_ids, proba=False, palci=False):
    
    exe_file_path = request.session["zoom_exe_path"]
    
    warnings.filterwarnings("ignore", message="The window has not been focused due to")

    zoom_app = (Application(backend="uia")
                .start(exe_file_path)
                .connect(title="Zoom", timeout=100))
    
    time.sleep(3)
    
    last_id = load_ids[-1]
    
    for load_id in load_ids:
        
        if cache.get("stop_action"):
            zoom_app.kill()
            messages.warning(request, f"You stopped sending messages!")
            return
    
        load = Load.objects.get(id=load_id)
        truck_drivers = load.drivers.all()
        
        message1 = load.message + request.user.landstar_info1()
        message2 = load.message + request.user.landstar_info2()
        message3 = request.user.load_offer_str() + message1 
        message4 = request.user.load_offer_str() + message2

        messages_zoom = [message1, message2, message3, message4]

        try:
            phone_tab = zoom_app.Zoom.child_window(title_re="Phone.*", control_type="TabItem").wrapper_object()
            phone_tab.click_input()

            sms_tab = zoom_app.Zoom.child_window(title_re="SMS.*", control_type="TabItem").wrapper_object()
            sms_tab.click_input()
            
            # message needs to be ready for Zoom application if type_keys is hit:
            if palci:
                messages_zoom = [message.replace("\n", "+{ENTER}").replace(" ", "{SPACE}") for message in messages_zoom] 

            for idx, driver in enumerate(truck_drivers):
                # If user press Esc it will stop the action after sending last message
                if cache.get("stop_action"):
                    zoom_app.kill()
                    messages.warning(request, f"You stopped sending messages!")
                    return

                if not driver.sms_sent:
                    new_sms = zoom_app.Zoom.child_window(title="New SMS", control_type="Button",
                                                        found_index=0).wrapper_object()
                    new_sms.click_input()

                    send_to = zoom_app.Zoom.child_window(title_re="Send to.*", control_type="Edit",
                                                        found_index=0).wrapper_object()
                    send_to.click_input()
                    
                    send_to.type_keys("^a{BACKSPACE}")
                    
                    if palci:
                        send_to.type_keys(driver.phone_number)
                    else:
                        pyperclip.copy(driver.phone_number)
                        send_to.type_keys("^v")
                        
                    send_to.type_keys("{ENTER}")

                    text = zoom_app.Zoom.child_window(title_re="Text.*", found_index=0).wrapper_object()
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

                    send_message = zoom_app.Zoom.child_window(title_re="Ctrl+.*", control_type="Button",
                                                            found_index=0).wrapper_object()
                    
                    if cache.get("stop_action"):
                        zoom_app.kill()
                        messages.warning(request, f"You stopped sending messages!")
                        return
                
                    if not proba:
                        send_message.click_input()
                        driver.sms_sent = True
                        driver.save()
                        time.sleep(0.5)
                    else:
                        text.type_keys("^a{BACKSPACE}")
                        
            # If everything went ok without stopping action
            if not cache.get("stop_action") and not proba:
                # Load is finished, but not deleted
                load.finished = True
                load.save()
                # Log history object is also created
                LogHistory.objects.create(load_id=load_id, drivers_informed_count=len(truck_drivers))
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
            