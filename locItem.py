from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import time 

ca_zip_codes = [95054, 96017, 95959, 93610, 93238, 92223, 92243]  # Example zip codes for California

def findLoc(locs):
    scroll_bar = driver.find_element(By.ID, 'mCSB_1_dragger_vertical')
    #loop through each one of location-item
    for n in range(6 , len(locs)+1): 
        id = "location-item-{}".format(n)
        block = driver.find_element(By.ID, id)

        #try to click the element
        try:
            block.click()
        #if it does not work, scroll page down and click
        except :
            action.drag_and_drop_by_offset(scroll_bar, 0, 25).perform()
            block.click()
   
        soup(id)
        block.click()

def soup(id):
    attributes = ["name", "is-member", "address", "address1", "phone", "email", "list-unstyled facility-details-list", "list-unstyled services-list", "list-unstyled shooting-av-list", "list-unstyled distance-list", "list-unstyled competitions-available-list"]
    soup = BeautifulSoup(driver.page_source,'lxml')
    attributes = soup.find_all("div", {"class": id})
    for attr in attributes:
        name = attr["name"]

    print(soup.find_all('span')) 



#url of the website to be scraped
url = "https://www.wheretoshoot.org/"
wait_time=4
delay_time=0.1

# Set driver as a Chrome driver
driver = webdriver.Chrome("C./chromedriver")
action = ActionChains(driver)
# access the website
driver.get(url)
#driver.maximize_window()

#wait for the page to be loaded
driver.implicitly_wait(wait_time)
dropdown = driver.find_element(By.XPATH, '//*[@id="dropdownMenu1"]')
dropdown.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="miles"]/ul/li[6]/a')))
time.sleep(2)
driver.implicitly_wait(wait_time)
first_option = driver.find_element(By.XPATH, '//*[@id="miles"]/ul/li[6]')
driver.execute_script("arguments[0].scrollIntoView(true);", first_option)
first_option.click()
driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
dropdown.click()
time.sleep(3)
search = driver.find_element(By.XPATH,'//*[@id="search"]')

for zip in ca_zip_codes:
    search.send_keys(zip)
    time.sleep(2)
    search.send_keys(Keys.ARROW_DOWN)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    locs = driver.find_elements(By.CLASS_NAME,'location-item')
    findLoc(locs)
    search.clear()
    time.sleep(5)


