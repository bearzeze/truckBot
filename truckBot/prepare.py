import time
import os
import re
import django

from django.core.cache import cache
from django.contrib import messages
from django.db import IntegrityError

from .models import LaneLoad

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

def preparing_loads(request, company, headless=True):
    
    if cache.get(f"lane_info_{company}_txt_path") is None:
        cache.set(f"lane_info_{company}_txt_path", request.user.landstar_credentials_path.replace("landstar", f"lane_info_{company}"), None)
    
    txt_path = cache.get(f"lane_info_{company}_txt_path")
    
    try:
        with open(txt_path, "r") as txt_file:
            DOM_content = txt_file.read()

    except:
        messages.error(request, f"File 'lane_info_{company}.txt' not found") 
        return
        
    if len(DOM_content) == 0:
        messages.warning(request, f"File 'lane_info_{company}.txt' is empty!")
        return
    
    soup = BeautifulSoup(DOM_content, "html.parser")
    
    # Scraping Navisphere
    if company == "Navisphere":
        scrape_navisphere(request, soup)
    

def scrape_navisphere(request, soup):
    lane_loads = soup.find_all(class_="find-loads-result") 
    messages.success(request, f"Total of {len(lane_loads)} lane loads found initially!")
    
    loads_saved = 0
    
    POSSIBLE_EQUIPMENT_TYPES = ["VAN","REFR", "FLAT"]
    
    for index, data in enumerate(lane_loads):
        origin = data.find(class_="js-load-origin")
        destination = data.find(class_="js-load-destination")
        
        origin_location = origin.find(class_="city-state-country-formatter").text
        destination_location = destination.find(class_="city-state-country-formatter").text
        pickup_date = origin.find(class_="time").find("span").text
        delivery_date = destination.find(class_="time").find("span").text
        
        requirments = data.find(class_="find-loads-result-requirements")
        start_stop_numb = requirments.find(class_="js-load-stop-count").find("span").text.split(", ")
        pick_numb, drop_numb = int(start_stop_numb[0].split(" ")[0]), int(start_stop_numb[1].split(" ")[0])
        miles = requirments.find(class_="js-load-distance").find("span").text.split(" ")[0].replace(",","")
        weight = requirments.find(class_="js-load-weight").find("span").text.split(" ")[0].replace(",","")
        equipments = requirments.find(class_="js-load-equipment-type").find_all("span")
        types = [type_.upper() for type_ in equipments[0].text.replace("Reefer", "Refr").replace("Flatbed", "Flat").split(", ")]
        length = int(equipments[1].text[0:2]) #Two numbers are enough for the length (48, 53, ...)
        
        
        if not (pick_numb == drop_numb == 1):
            messages.warning(request, f"Load from {origin_location} to {destination_location} has more than one pick or drop ({pick_numb}p, {drop_numb}d)!")
            continue
        
        # Checking possible equipment types:
        if not all(equipment_type in POSSIBLE_EQUIPMENT_TYPES for equipment_type in types):
            messages.warning(request, f"Only next equipment types are taken in consideration for posting: {', '.join(POSSIBLE_EQUIPMENT_TYPES)}. "+ 
                             f"This load require(s): {', '.join(types)}")
            continue
         
        
        # If there is no price, that load needs to be skipped
        try:
            price = data.find(class_="js-load-rate").find("h4").text.split(" ")[0].replace(",", "")
        except AttributeError:
            messages.warning(request, f"Load from {origin_location} to {destination_location} does not have an established rate!")
            continue
        
        # Preparing data about Equipment type compatible for the Landstar form 
        types = ",".join(types)
        if length != 1:
            types = types.replace("VAN", f"{length}VN").replace("FLAT", f"{length}FL")
        
        # Saving load into database, which is prepared for posting on landstar
        try:
            load = LaneLoad(user = request.user,
                            origin = origin_location.replace(", ", ","),
                            destination = destination_location.replace(", ", ","),
                            pickup = pickup_date,
                            delivery = delivery_date,
                            miles = miles,
                            weight = weight,
                            equipment = types,
                            price = price)
            load.save()
            
        except IntegrityError:
            messages.warning(request, f"Load {load} is already in the database!")
            
        else:
            loads_saved += 1

        
    messages.success(request, f"In total {loads_saved} load(s) saved in database for posting on Landstar!")
         
           
                
