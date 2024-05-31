import json
import os
import platform

from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, JsonResponse

if platform.system() == "Windows":
    from pynput.keyboard import Key, Listener
    from .zoom import send_sms

from .scrape import scrape_trucks
from .models import User, LogHistory, Load
from .serializers import LogHistorySerializer


@login_required
def index(request):
    loads_db = Load.objects.filter(finished=False)
    load_data = []
    
    for load in loads_db:
        all_drivers = load.drivers.count()
        informed_drivers = load.drivers.filter(sms_sent=True).count()
        load_data.append({
            "load": load,
            "total_drivers": all_drivers,
            "informed_drivers": informed_drivers
        })
        
    return render(request, "truckBot/index.html", context={
        "loads": load_data,
    })


# Method for scraping the website in order to get information about loads and available drivers
@login_required
def scrape(request):
    print(platform.system())

    if request.method == "POST" and request.user.is_authenticated and platform.system() == "Windows":
        
        radius_distance = request.POST.get("radius-distance");
        
        load_ids = request.POST.get("load_ids")
        try:
            if len(load_ids) == 0:
                raise
            
            load_ids = [int(load_id.strip()) for load_id in load_ids.split(",")]
            
        except ValueError:
            messages.error(request, "Load ids must be integers separated by commas")
            return HttpResponseRedirect(reverse("index"))
        
        load_ids_copy = load_ids.copy()
        
        # Checking first and if load_id is already processed/scraped it will be removed from the list:
        for load_id in load_ids_copy:
            # If this load is in Log History you cannot scrape it again
            if LogHistory.objects.filter(load_id=load_id).exists():
                messages.warning(request, f"Load with {load_id} id had been already processed (find it in Log history)")
                load_ids.remove(load_id)
                continue
                
            # If this load is in Loads database you cannot scrape it again
            if Load.objects.filter(id=load_id).exists():
                messages.warning(request, f"Load with {load_id} id is already prepared!")
                load_ids.remove(load_id)

        # Checks whether scrape is aborted during the process
        if cache.get("abort_scraping"):
            messages.warning(request, 'Scraping aborted!')
            
        try:
            headless = True
            
            if request.user.is_superuser:
                headless = False
                
            scrape_trucks(request, load_ids, radius_distance, headless)
                                
        except Exception as e:
            return HttpResponseRedirect(reverse("index"))
            
        cache.set('is_scraping', False, None)
        cache.set('abort_scraping', False, None)

    return HttpResponseRedirect(reverse("index"))


# API for aborting the scraping process
@login_required
def set_scraping_flag(request):
    if request.method == 'POST' and request.user.is_authenticated:
        cache.set('is_scraping', True, None)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
    
@login_required
def set_abort_flag(request):
    if request.method == 'POST' and request.user.is_authenticated:
        cache.set('abort_scraping', True, None)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

# Sending messages to the driver using Zoom app
@login_required
def send_messages(request):
    if request.method == "POST" and request.user.is_authenticated:
        
        load_ids = request.POST.getlist('scraped_ids')
        
        # If there are no loads it redirects to the home page
        if (len(load_ids) == 0 ):
            return HttpResponseRedirect(reverse("index"))
        
        # If esc is pressed it stops the action 
        cache.set("stop_action", False, None)        
        listener = Listener(on_press=on_press)
        listener.start()
        
        # Filtering only ids which will be processed for sending
        load_ids_copy = load_ids.copy()
        for load_id in load_ids_copy:
            # Checking whether load exists in db
            if not Load.objects.filter(id=load_id).exists():
                messages.error(request, f"There is no scraped load with id {load_id}")
                load_ids.remove(load_id)
            
        # Method for sending sms through the zoom
        send_sms(request, load_ids, proba=False, palci=False)
    
        listener.stop()
    
    return HttpResponseRedirect(reverse("index"))


# API for changing the load message
@login_required
def change_load_message(request, load_id):
    if request.method == "PUT" and request.user.is_authenticated:
        try:
            load = Load.objects.get(id=load_id)
        except:
            return JsonResponse({"error": "Load doesn't exists."}, status=404)

        data = json.loads(request.body)
            
        new_message = data.get("message")
        if not new_message in ["", None]:
            load.message = data.get("message")
            load.save()
            return JsonResponse({"success": f"Load with id {load_id} has new message.", "message": new_message}, status=200)
        else:
            return JsonResponse({"error": "Message cannot be empty."}, status=400)
  

# API for getting all the log through the Serializer
@login_required
def log_history(request):
    if request.method == "GET" and request.user.is_authenticated:
        logs = LogHistory.objects.all().order_by("-date")
        serializer = LogHistorySerializer(logs, many=True)
        return JsonResponse(serializer.data, safe=False)
        
  
# Profile page
@login_required
def profile(request):
    try:
        profile = User.objects.get(username=request.user.username)  
        message = None 
                    
        if request.method == "POST":
            form_type = request.POST.get("form_type")
            
            if form_type == "truckBot":
                true_current_password = profile.password
                
                current_pass = request.POST.get("truck_current_password")
                new_pass = request.POST.get("truck_new_password")
                confirm_pass = request.POST.get("truck_confirm_password")
                
                if not check_password(current_pass, true_current_password):
                    message = {
                        "content": "You didn't type the current password correctly! Please try again.",
                        "style": "danger"
                    }
                
                elif check_password(new_pass, true_current_password):
                    message = {
                        "content": "Your new password cannot be the same as your old password! Please choose a different password.",
                        "style": "warning"
                    }
                    
                elif new_pass != confirm_pass:
                    message = {
                        "content": "The password and confirmation password do not match! Please try again.",
                        "style": "danger"
                    }
                    
                elif len(new_pass) < 6:
                    message = {
                        "content": "Password needs to have at least 6 characters! Please try again.",
                        "style": "danger"
                    }
                    
                else:
                    profile.set_password(new_pass)
                    profile.save()
                    update_session_auth_hash(request, profile)
                    message = {
                        "content": "Password has been changed.",
                        "style": "success"
                    }
                
            elif form_type == "zoom":
                new_zoom_exe_path = request.POST.get("zoom_exe")
                new_zoom_number = request.POST.get("zoom_phone_num")
                
                new_path = False
                if os.path.exists(new_zoom_exe_path):
                    
                    if not new_zoom_exe_path.endswith("Zoom.exe"):
                        message = {
                        "content": f"Your path needs to end with 'Zoom.exe'!",
                        "style": "danger"
                    }
                        
                    elif new_zoom_exe_path != profile.zoom_exe_path:
                        new_path = True
                        content = "zoom.exe path has been changed."
                        profile.zoom_exe_path = new_zoom_exe_path
                        request.session["zoom_exe_path"] = profile.zoom_exe_path
                        
 
                else:
                    message = {
                        "content": f"'{new_zoom_exe_path}' path doesn't exists!",
                        "style": "danger"
                    }

                new_numb = False
                if new_zoom_number != profile.zoom_phone_numb:
                    new_numb = True
                    content = "Zoom phone number has been changed."
                    profile.zoom_phone_numb = new_zoom_number
                    request.session["zoom_phone_num"] = new_zoom_number
                        
                if new_numb and new_path:
                    content = "Zoom exe file and phone number have been changed."

                
                if new_numb or new_path:
                    message = {
                        "content": content,
                        "style": "success"
                    }
                    profile.save()
                        
            elif form_type == "landstar":
                new_first_name = request.POST.get("landstar_firstname")
                new_last_name = request.POST.get("landstar_lastname")
                new_credentials_path = request.POST.get("landstar_credentials")
                
                new_name = False
                new_path = False
                
                if new_first_name != profile.landstar_firstname:
                    profile.landstar_firstname = new_first_name.title()
                    content = "Landstar name is changed."
                    new_name = True
                    
                if new_last_name != profile.landstar_lastname:
                    profile.landstar_lastname = new_last_name.title()
                    content = "Landstar name is changed."
                    new_name = True
                
                if os.path.exists(new_credentials_path):  
                    if not new_credentials_path.endswith(".txt"):
                        message = {
                        "content": f"You need to specify path of the textual file (.txt) where credentials are!",
                        "style": "danger"
                    }
                    elif new_credentials_path != profile.landstar_credentials_path:
                        new_path = True
                        content = "Landstar credentials path has been changed."
                        profile.landstar_credentials_path = new_credentials_path
                        load_landstar_credentials(request, new_credentials_path)

                else:
                    message = {
                        "content": f"'{new_credentials_path}' path doesn't exists!",
                        "style": "danger"
                    }
                    
                if new_path and new_name:
                    content = "Landstar name and credentials path have been changed."
                    
                if new_path or new_name:
                    message = {
                        "content": content,
                        "style": "success"
                    }
                    profile.save()
                     
        return render(request, "truckBot/profile.html", context={
                "profile": profile,
                "message": message})
            
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
              

def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "truckBot/login.html", context={
                "message": "Invalid username/password"
            })
        else:
            login(request, user)
            
            # Loading landstar credentials
            load_landstar_credentials(request, user.landstar_credentials_path)
            request.session["zoom_exe_path"] = user.zoom_exe_path
            request.session["zoom_phone_num"] = user.zoom_phone_numb
                
            return HttpResponseRedirect(reverse("index"))

    elif request.method == "GET":
        return render(request, "truckBot/login.html")
    
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def no_page(request, everything_else):
    return render(request, "truckBot/noPage.html")
    
    
def load_landstar_credentials(request, landstar_credentials_path):
    if landstar_credentials_path:
        with open(landstar_credentials_path, "r") as file:
            request.session["landstar_acc"] = file.readline().strip()
            request.session["landstar_pass"] = file.readline().strip()
  
            
# Function for listening the keys      
def on_press(key):
    if key == Key.esc:
        cache.set("stop_action", True, None)