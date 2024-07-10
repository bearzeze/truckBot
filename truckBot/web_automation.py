import time
import os
import re
import pyperclip
import django

from django.core.cache import cache
from django.contrib import messages

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from .models import Driver, Load, LaneLoad, PostHistory


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

    
# Method for scraping load and truck drivers info on Landstar
def scrape_trucks(request, load_ids, radius, headless=True):
    landstar = LandstarAutomation(request, "scraping", headless)

    first_iter, last_iter = False, False
    first_id, last_id = load_ids[0], load_ids[-1]
    close = False
    
    print(load_ids)
    
    for load_id in load_ids:
        
        first_iter = load_id == first_id
        last_iter = load_id == last_id
        
        print(load_id)
    
        try:
            # Login only at first iteration
            if first_iter:
                # First log in
                if not landstar.login():
                    return  
                          
            if landstar.check_for_aborting():
                return 

            # Set information for load and search for available trucks
            landstar.search_available_trucks(load_id, radius)
            
            if landstar.check_for_aborting():
                return 

            result = landstar.load_and_drivers_info()
            
            if result == "Load ID doesn't exists":
                messages.error(request, f"Load with {load_id} id doesn't exist!")
                continue
            
            if landstar.check_for_aborting():
                return 
            
            # Extracting info about drivers and load 
            load_info_rows, driver_table = result
            
            # Getting the weight of a load
            weight = landstar.finding_load_weight(load_id)
        
            if landstar.check_for_aborting():
                return  
            
            # Creating load in the database
            landstar.saving_load_in_db(load_id, load_info_rows, weight)
            
            # Creating drivers in the database
            landstar.saving_drivers_in_db(load_id, driver_table)
            
            messages.success(request, f"Load with {load_id} id is successfully saved in database!")
            

        except Exception as e:
            messages.error(request, f"Load with {load_id} id had not been scraped due to the error: {e}!")
            close = True
            raise

        finally:
            if last_iter or cache.get("abort_scraping") or close:
                landstar.driver.quit()
    
    # This will delete ids from cache which are defined into input field on home page
    else:
        cache.set('ids', "", None)


# Method for posting loads on Landstar
def posting_loads_landstar(request, load_ids, max_tabs=1, headless=True):
    loads = LaneLoad.objects.filter(id__in=load_ids)
    
    try:
        landstar = LandstarAutomation(request, "posting", headless)
        
        if landstar.check_for_aborting():
            return 

        if not landstar.login():
            return
        
        if landstar.check_for_aborting():
            return 
        
        time.sleep(3)
        
        landstar.posting_loads(loads, max_tabs)
        
    except Exception as e:
        messages.error(request, f"Posting stopped due to an error: {e}")
        print(e)
        
    finally:
        landstar.driver.quit()
    
         

# class about Landstar
class LandstarAutomation:
    def __init__(self, request, action, headless):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
    
        if headless:
            chrome_options.add_argument("--headless")  # Ensure GUI is off
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.request = request
        self.action = action.title()
       
        
    def login(self):
        self.driver.get("https://www.landstaronline.com/Public/Login.aspx#")

        # To find the element with id 'USER'
        username_field = self.driver.find_element(By.ID, "USER")

        # To find the element with id 'PASSWORD'
        password_field = self.driver.find_element(By.ID, "PASSWORD")

        wait = WebDriverWait(self.driver, 2)

        username_field.send_keys(self.request.session["landstar_acc"])
        password_field.send_keys(self.request.session["landstar_pass"])

        login_btn = self.driver.find_element(By.ID, "Submit")
        login_btn.click()
        
        try:
            failure_element = self.driver.find_element(By.ID, "LoginFailureWarning")
            messages.error(self.request, f"{failure_element.text}")
            return None
        except:
            return "Ok"
        
    
    def search_available_trucks(self, load_id, radius):
        self.driver.get(f"https://www.landstaronline.com/AvailableTrucks?loadid={load_id}&agency=SYE&sourcesystem=DIGEX")

        # Set information
        max_result = self.driver.find_element(By.ID, "MaxResults")
        self.driver.execute_script("arguments[0].value = 500", max_result)

        capacity_type = self.driver.find_element(By.ID, "CapacityTypes")
        self.driver.execute_script("arguments[0].value = 1", capacity_type)

        distance_radius = self.driver.find_element(By.ID, "RadiusDistances")
        self.driver.execute_script(f"arguments[0].value = {radius}", distance_radius)

        # time for visual checking
        time.sleep(2)

        # Search for available trucks
        search_btn = self.driver.find_element(By.ID, "BtnSearch")
        search_btn.click()       
       
       
    def load_and_drivers_info(self):
            # It is continuation of previous method
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'SearchResultsGrid')))

            time.sleep(3)

            # Scrape info for the truck drivers message and save in database as Driver objects
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            parent_div = soup.find(id="SearchResultsGrid")
            driver_table = parent_div.find('tbody')
            
            # Find the div with the class "header header2"
            div = soup.find('div', {'class': 'header header2'})

            # Extract the load ID using a regular expression
            load_ID_scrapped = re.search(r'Load\s*#\s*(\d+)', div.text).group(1).strip()
            
            if int(load_ID_scrapped) == 0:
                return "Load ID doesn't exists"
            
            
            driver_table = driver_table.find_all('tr')
            
            # Scrape info for the load message and save in database as Load object
            parent_div = soup.find(id="tblLoadInfo")
            load_table = parent_div.find("tbody")
            table_rows = load_table.find_all("tr")
            
            return table_rows, driver_table
       
       
    def finding_load_weight(self, load_id):
        self.driver.get(f"https://leads.landstaronline.com/AvailableLoads/CommoditiesView.aspx?loadid={load_id}")
        weight_row = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")))

        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        data = soup.find(id="ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")
        weight = data.find_all("td")[6].text
        return weight
     
     
    def saving_load_in_db(self, load_id, load_info, weight):
        Load.objects.create(id=load_id,
                    user=self.request.user,
                    origin=load_info[0].find_all("td")[3].text.strip(),
                    destination=load_info[1].find_all("td")[3].text.strip(),
                    pickup=load_info[0].find_all("td")[5].text.strip(),
                    delivery=load_info[1].find_all("td")[5].text.strip(),
                    mode=load_info[2].find_all("td")[5].text.strip(),
                    miles=int(load_info[2].find_all("td")[3].text.strip()),
                    weight=int(weight),
                    price=load_info[2].find_all("td")[1].text.strip()
                )
        
        
    def saving_drivers_in_db(self, load_id, driver_table):
        if driver_table[0].text != "No available trucks found meeting the specified search criteria.":
                for row in driver_table:
                    cells = row.find_all('td')

                    # Only drivers with phone numbers are important
                    if len(cells[5].text) > 7:
                        Driver.objects.create(name=cells[4].text,
                                            phone_number=cells[5].text.strip().strip('\xa0')[:14], # 14 digits is the phone number
                                            load=Load.objects.get(id=load_id))
        
    
    def check_for_aborting(self):
        if cache.get("abort_scraping"):
            messages.warning(self.request, f'{self.action} aborted!')
        
        return cache.get("abort_scraping")
    
    
    def extract_phone_numb_post(self):
            numbers_only = re.sub(r"\D", "", self.request.user.zoom_phone_numb)
            return f"({numbers_only[:3]}) {numbers_only[3:6]}-{numbers_only[6:]}"
    
       
    def create_state_dict_abbr(self):
        state_dict = {
            'AL': 'ALABAMA',
            'AK': 'ALASKA',
            'AZ': 'ARIZONA',
            'AR': 'ARKANSAS',
            'CA': 'CALIFORNIA',
            'CO': 'COLORADO',
            'CT': 'CONNECTICUT',
            'DE': 'DELAWARE',
            'DC': 'DIST. COLUMBIA',
            'FL': 'FLORIDA',
            'GA': 'GEORGIA',
            'HI': 'HAWAII',
            'ID': 'IDAHO',
            'IL': 'ILLINOIS',
            'IN': 'INDIANA',
            'IA': 'IOWA',
            'KS': 'KANSAS',
            'KY': 'KENTUCKY',
            'LA': 'LOUISIANA',
            'ME': 'MAINE',
            'MD': 'MARYLAND',
            'MA': 'MASSACHUSETTS',
            'MI': 'MICHIGAN',
            'MN': 'MINNESOTA',
            'MS': 'MISSISSIPPI',
            'MO': 'MISSOURI',
            'MT': 'MONTANA',
            'NE': 'NEBRASKA',
            'NV': 'NEVADA',
            'NH': 'NEW HAMPSHIRE',
            'NJ': 'NEW JERSEY',
            'NM': 'NEW MEXICO',
            'NY': 'NEW YORK',
            'NC': 'NORTH CAROLINA',
            'ND': 'NORTH DAKOTA',
            'OH': 'OHIO',
            'OK': 'OKLAHOMA',
            'OR': 'OREGON',
            'PA': 'PENNSYLVANIA',
            'PR': 'PUERTO RICO',
            'RI': 'RHODE ISLAND',
            'SC': 'SOUTH CAROLINA',
            'SD': 'SOUTH DAKOTA',
            'TN': 'TENNESSEE',
            'TX': 'TEXAS',
            'UT': 'UTAH',
            'VT': 'VERMONT',
            'VA': 'VIRGINIA',
            'WA': 'WASHINGTON',
            'WV': 'WEST VIRGINIA',
            'WI': 'WISCONSIN',
            'WY': 'WYOMING'
        }
        
        return state_dict
         
             
    def posting_loads(self, loads, max_tabs):
        
        numb_loads = len(loads)
        # Max_tabs cannot be greater than number of loads
        max_tabs = min(numb_loads, max_tabs)
        
        # state_dict {abbrivation: state}
        state_dict = self.create_state_dict_abbr()
        
        phone_num = self.extract_phone_numb_post()
        pyperclip.copy(phone_num)

        # Opening max_tab - 1 (already there is one tab opened) number of tabs 
        for _ in range(max_tabs - 1):
            self.driver.execute_script("window.open('', '_blank');")
        
        # Posting max_tab number of loads at same time into max_tab numb of tabs
        for i in range(0, numb_loads, max_tabs):
            # If numb_loads % max_tab != 0 then on last iteration of outer loop will have less loads then max_tabs
            loop_limit = max_tabs if numb_loads - i >= max_tabs else numb_loads - i 
            
            if self.check_for_aborting():
                return
            
            for j in range(0, loop_limit):
                try:
                    load = loads[i + j]
                    load_origin = [elem.upper() for elem in load.origin.split(',')]
                    load_destination = [elem.upper() for elem in load.destination.split(',')]
                    load_equipment = load.equipment.split(',')
                    
                    
                    self.driver.switch_to.window(self.driver.window_handles[j])
                    self.driver.get("https://leads.landstaronline.com/AvailableLoads/AvailableLoadsListView.aspx")
                    new_load = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_NavigationBar1_rgNew_rbNewAvailableLoad')
                    new_load.click()
                    
                    time.sleep(1)
                    
                    if self.check_for_aborting():
                        return
                    
                    callback = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_txtContactNumber')
                    callback.send_keys(Keys.CONTROL + "a")
                    callback.send_keys(Keys.CONTROL + "v")
                    
                    # Origin details
                    origin_state = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_cbxOriginState_Input')
                    origin_state.send_keys(Keys.CONTROL + "a")
                    origin_state.send_keys(state_dict[load_origin[1]] + Keys.ENTER)

                    origin_city = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_cbxOriginCity_Input')
                    origin_city.send_keys(load_origin[0] + Keys.ENTER)
                    
                    # Pick up date details
                    pickup_date_from = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_calOriginPickupFromDate_dateInput')
                    pickup_date_from.send_keys(Keys.CONTROL + "a")
                    pickup_date_from.send_keys(load.pickup + Keys.ENTER)
                    pickup_date_thru = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_calOriginPickupThruDate_dateInput')
                    pickup_date_thru.send_keys(Keys.CONTROL + "a")
                    pickup_date_thru.send_keys(load.pickup + Keys.ENTER)
                    
                    # Destination details
                    destination_state = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_cbxDestinationState_Input')
                    destination_state.send_keys(Keys.CONTROL + "a")
                    destination_state.send_keys(state_dict[load_destination[1]] + Keys.ENTER)
                    
                    destination_city = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_cbxDestinationCity_Input')
                    destination_city.send_keys(load_destination[0] + Keys.ENTER)
                    
                    # Delivery date details
                    delivery_date_from = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_calDestinationDropFromDate_dateInput')
                    delivery_date_from.send_keys(Keys.CONTROL + "a")
                    delivery_date_from.send_keys(load.delivery + Keys.ENTER)
                    delivery_date_from = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_calDestinationDropThruDate_dateInput')
                    delivery_date_from.send_keys(Keys.CONTROL + "a")
                    delivery_date_from.send_keys(load.delivery + Keys.ENTER)
                                        
                    # Weight and rate
                    weight_element = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_txtWeight')
                    weight_element.send_keys(Keys.CONTROL + "a")
                    weight_element.send_keys(load.weight)
                    
                    rate_element = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_txtRate')
                    rate_element.send_keys(Keys.CONTROL + "a")
                    rate_element.send_keys(load.price)
                    
                    # Equipment
                    equipment_list = [self.driver.find_element(By.ID, f'ctl00_ctl00_SiteMasterContent_PageContent_txtType{num}') for num in range (1, 4)]
                    
                    # Clearing equipment field from initial values
                    for i in range(2, -1, -1):
                        equipment_list[i].click()
                        equipment_list[i].send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
                        
                    # Filling equipment with load equipments
                    for i in range(0, len(load_equipment)):
                        equipment_list[i].click()
                        equipment_list[i].send_keys(load_equipment[i])
                    
                    time.sleep(1)
                    
                    if self.check_for_aborting():
                        return
                    
                    post_button = self.driver.find_element(By.ID, 'ctl00_ctl00_SiteMasterContent_NavigationBar1_rgCommands_rbSubmit_Item')
                    post_button.click()
                    time.sleep(2)
                    
                    load_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_SiteMasterContent_PageContent_confirmationLink')))
                    load_id = load_id.text
                    
                    load.posted = True
                    load.landstar_id = load_id
                    
                    load.save()
                    messages.success(self.request, f"Load '{load}' was posted on Landstar with the id = {load_id}")
                    
                    # If everything went ok PostHistory object is created
                    PostHistory.objects.create(user=self.request.user,
                                               load_description=load.history(),
                                               landstar_id=load_id)
                    
                except Exception as e:
                    messages.error(self.request, f"Load '{load}' was not posted due to an error: {e}")
                
            
            time.sleep(1)
        
        

                