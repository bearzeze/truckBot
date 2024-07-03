import time
import os
import re
import django

from django.core.cache import cache
from django.contrib import messages

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from .models import Driver, Load


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

# Method for scraping
def scrape_trucks(request, load_ids, radius, headless=True):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    if headless:
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    
    first_iter, last_iter = False, False
    first_id, last_id = load_ids[0], load_ids[-1]
    
    for load_id in load_ids:
        
        if load_id == last_id:
            last_iter = True
            
        if load_id == first_id:
            first_iter = True
        else:
            first_iter = False
    
        try:
            # Login only at first iteration
            if first_iter:
            # First log in
                driver.get("https://www.landstaronline.com/Public/Login.aspx#")

                # To find the element with id 'USER'
                username_field = driver.find_element(By.ID, "USER")

                # To find the element with id 'PASSWORD'
                password_field = driver.find_element(By.ID, "PASSWORD")

                wait = WebDriverWait(driver, 2)

                username_field.send_keys(request.session["landstar_acc"])
                password_field.send_keys(request.session["landstar_pass"])

                login_btn = driver.find_element(By.ID, "Submit")
                login_btn.click()
            
            if cache.get("abort_scraping"):
                messages.warning(request, 'Scraping aborted!')
                return 

            # Set information for load and search for available trucks
            driver.get(f"https://www.landstaronline.com/AvailableTrucks?loadid={load_id}&agency=SYE&sourcesystem=DIGEX")

            # Set information
            max_result = driver.find_element(By.ID, "MaxResults")
            driver.execute_script("arguments[0].value = 500", max_result)

            capacity_type = driver.find_element(By.ID, "CapacityTypes")
            driver.execute_script("arguments[0].value = 1", capacity_type)

            distance_radius = driver.find_element(By.ID, "RadiusDistances")
            driver.execute_script(f"arguments[0].value = {radius}", distance_radius)

            # time for visual checking
            time.sleep(5)

            # Search for available trucks
            search_btn = driver.find_element(By.ID, "BtnSearch")
            search_btn.click()
            
            if cache.get("abort_scraping"):
                messages.warning(request, 'Scraping aborted!')
                return 

            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'SearchResultsGrid')))

            time.sleep(5)

            # Scrape info for the truck drivers message and save in database as Driver objects
            soup = BeautifulSoup(driver.page_source, "html.parser")
            parent_div = soup.find(id="SearchResultsGrid")
            driver_table = parent_div.find('tbody')
            
            # Find the div with the class "header header2"
            div = soup.find('div', {'class': 'header header2'})

            # Extract the load ID using a regular expression
            load_ID_scrapped = re.search(r'Load\s*#\s*(\d+)', div.text).group(1).strip()
            
            if int(load_ID_scrapped) == 0:
                messages.error(request, f"Load with {load_id} id doesn't exist!")
                continue
            
            if cache.get("abort_scraping"):
                messages.warning(request, 'Scraping aborted!')
                return 
            
            driver_table = driver_table.find_all('tr')

            # Scrape info for the load message and save in database as Load object
            parent_div = soup.find(id="tblLoadInfo")
            load_table = parent_div.find("tbody")

            # Getting the weight of a load
            driver.get(f"https://leads.landstaronline.com/AvailableLoads/CommoditiesView.aspx?loadid={load_id}")
            weight_row = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")))

            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            data = soup.find(id="ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")
            weight = data.find_all("td")[6].text
            
            # Creating load in the database
            rows = load_table.find_all("tr")
            
            if cache.get("abort_scraping"):
                messages.warning(request, 'Scraping aborted!')
                return 
            
            Load.objects.create(id=load_id,
                                user=request.user,
                                origin=rows[0].find_all("td")[3].text.strip(),
                                destination=rows[1].find_all("td")[3].text.strip(),
                                pickup=rows[0].find_all("td")[5].text.strip(),
                                delivery=rows[1].find_all("td")[5].text.strip(),
                                mode=rows[2].find_all("td")[5].text.strip(),
                                miles=int(rows[2].find_all("td")[3].text.strip()),
                                weight=int(weight),
                                price=rows[2].find_all("td")[1].text.strip()
                            )
            
            # Creating drivers in the database
            if driver_table[0].text != "No available trucks found meeting the specified search criteria.":
                for row in driver_table:
                    cells = row.find_all('td')

                    # Only drivers with phone numbers are important
                    if len(cells[5].text) > 7:
                        Driver.objects.create(name=cells[4].text,
                                            phone_number=cells[5].text.strip().strip('\xa0')[:14], # 14 digits is the phone number
                                            load=Load.objects.get(id=load_id))
            
            messages.success(request, f"Load with {load_id} id is successfully saved in database!")

        except Exception as e:
            messages.error(request, f"Load with {load_id} id had not been scraped due to the error: {e}!")
            raise


        finally:
            if last_iter or cache.get("abort_scraping"):
                driver.quit()
    
    else:
        cache.set('ids', "", None)
