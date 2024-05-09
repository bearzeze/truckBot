from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import json
import os

from pywinauto.application import Application

from .models import User, Driver, LogHistory, Load


@login_required
def index(request):
    return render(request, "truckBot/index.html")


@login_required
def scrape(request):
    if request.method == "POST" and request.user.is_authenticated:
        load_ids = request.POST.get("load_ids")
        try:
            load_ids = [int(load_id.strip()) for load_id in load_ids.split(",")]
            print(load_ids)
        except ValueError:
            messages.error(request, "Load ids must be integers separated by commas")
                        
        
        
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
            return HttpResponseRedirect(reverse("index"))

    elif request.method == "GET":
        return render(request, "truckBot/login.html")
    
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


@login_required
def profile_info_change(request):
    
    return HttpResponseRedirect(reverse("index"))

