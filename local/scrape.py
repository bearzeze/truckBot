import datetime
import time
import selenium
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_auto_update.chrome_app_utils import ChromeAppUtils
from webdriver_auto_update.webdriver_manager import WebDriverManager
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


# Method for scraping
def scrape_trucks(load_id):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # First log in
        driver.get("https://www.landstaronline.com/Public/Login.aspx#")

        # To find the element with id 'USER'
        username_field = driver.find_element(By.ID, "USER")

        # To find the element with id 'PASSWORD'
        password_field = driver.find_element(By.ID, "PASSWORD")

        wait = WebDriverWait(driver, 2)

        username_field.send_keys("avolkov")
        password_field.send_keys("200kman")

        login_btn = driver.find_element(By.ID, "Submit")
        login_btn.click()

        # Set information for load and search for available trucks
        driver.get(f"https://www.landstaronline.com/AvailableTrucks?loadid={load_id}&agency=SYE&sourcesystem=DIGEX")

        # Set information
        max_result = driver.find_element(By.ID, "MaxResults")
        driver.execute_script("arguments[0].value = 500", max_result)

        capacity_type = driver.find_element(By.ID, "CapacityTypes")
        driver.execute_script("arguments[0].value = 1", capacity_type)

        distance_radius = driver.find_element(By.ID, "RadiusDistances")
        driver.execute_script("arguments[0].value = 200", distance_radius)

        # time for visual checking
        time.sleep(1)

        # Search for available trucks
        search_btn = driver.find_element(By.ID, "BtnSearch")
        search_btn.click()

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'SearchResultsGrid')))

        time.sleep(5)

        # Scrape truck drivers info and save to txt file
        soup = BeautifulSoup(driver.page_source, "html.parser")
        parent_div = soup.find(id="SearchResultsGrid")
        table = parent_div.find('tbody')
        save_truck_driver_info(table, load_id)

        # Scrape info for message and save as txt file
        parent_div = soup.find(id="tblLoadInfo")
        table = parent_div.find("tbody")

        # Getting the weight of a load
        driver.get(f"https://leads.landstaronline.com/AvailableLoads/CommoditiesView.aspx?loadid={load_id}")
        weight_row = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")))

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = soup.find(id="ctl00_ctl00_SiteMasterContent_PageContent_dgCommodities_ctl00__0")
        weight = data.find_all("td")[6].text
        create_message(table, weight, load_id)

        print("everything went ok!")

        load_scraped(load_id)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    finally:
        driver.quit()


def save_truck_driver_info(table, load_id):
    truck_drivers = list()
    table = table.find_all('tr')

    if table[0].text != "No available trucks found meeting the specified search criteria.":
        for row in table:
            cells = row.find_all('td')

            # Only not empty phone number, drivers are important
            if len(cells[5].text) > 7:
                truck_drivers.append({"name": cells[4].text,
                                      "phone_number": cells[5].text.strip().strip('\xa0')[:14], # 14 cifara broj
                                      "sms_sent": False})

    with open(f"./files/truck_infos/info_{load_id}.txt", "w") as file:
        json.dump(truck_drivers, file)


def create_message(table, weight, load_id):
    rows = table.find_all("tr")

    message_info = {
        "origin": rows[0].find_all("td")[3].text.strip(),
        "pickup_date": rows[0].find_all("td")[5].text.strip(),
        "destination": rows[1].find_all("td")[3].text.strip(),
        "delivery_date": rows[1].find_all("td")[5].text.strip(),
        "mode": rows[2].find_all("td")[5].text.strip(),
        "miles": rows[2].find_all("td")[3].text.strip(),
        "weight": weight,
        "rate": rows[2].find_all("td")[1].text.strip(),
    }

    with open(f"./files/messages/message_{load_id}.txt", "w") as file:
        message = (
            f"[[LOAD OFFER!!]][[LOAD OFFER!!]]\n" +
            f"Pick: {message_info['origin']} -- {message_info['pickup_date']}\n" +
            f"Delivery: {message_info['destination']} -- {message_info['delivery_date']}\n" +
            f"Mode: {message_info['mode']}\n" +
            f"Miles: {message_info['miles']}\n" +
            f"Est. Weight: {weight} lb\n" +
            f"RATE {message_info['rate']}\n" +
            f"Alex  Contact: 619-352-0887")

        file.write(message)


def get_message(load_id):
    with open(f"./files/messages/message_{load_id}.txt", "r") as file:
        message = file.read()

    return message


def get_truck_drivers(load_id):
    with open(f"./files/truck_infos/info_{load_id}.txt", "r") as file:
        data = json.load(file)

    return data


def load_scraped(id):
    with open("./files/scraped.txt", "a+") as file:
        file.write(f"{id}\t{datetime.datetime.now()}\n")


def check_load_scraped(id):
    filename = "./files/scraped.txt"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file.readlines():
                if id == int(line.split('\t')[0].strip()):
                    return True

    return False
