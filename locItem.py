from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import time 
import csv
#ca_zip_codes = [95054]
ca_zip_codes = [75001,75201, 75023] 
#ca_zip_codes = [96017, 95959, 93610, 93238, 92223, 92243]  # Example zip codes for California
unique_ids = set()
rows = []
def findLoc(locs):
    scroll_bar = driver.find_element(By.ID, 'mCSB_1_dragger_vertical')
    #loop through each one of location-item
    for n in range(1 , len(locs)+1): 
        id = "location-item-{}".format(n)
        block = driver.find_element(By.ID, id)
        try:
        #try to click the element
            try:
                block.click()
            #if it does not work, scroll page down and click
            except :
                try:
                    action.drag_and_drop_by_offset(scroll_bar, 0, 40).perform()
                    block.click()
                except:
                    # Find the inner div by its ID or class name
                    inner_div = driver.find_element(By.XPATH,'//*[@id="where-to-shoot"]/div[2]/div[2]/div[3]/div')  # or driver.find_element_by_class_name('inner-div')

                    # Get the height of the browser window
                    window_height = driver.execute_script('return window.innerHeight;')

                    # Get the initial height of the inner div
                    inner_div_height = inner_div.size['height']

                    # Scroll down until the bottom of the inner div is visible
                    while driver.execute_script('return window.scrollY + arguments[0] < arguments[1];', window_height, inner_div_height):
                        driver.execute_script('window.scrollBy(0, arguments[0]);', 40)
                        time.sleep(1)
                    block.click()
            soup(id)
            try:
                block.click()
            except :
                try:
                    action.drag_and_drop_by_offset(scroll_bar, 0, 40).perform()
                    block.click()
                except:
                    # Find the inner div by its ID or class name
                    inner_div = driver.find_element(By.XPATH,'//*[@id="where-to-shoot"]/div[2]/div[2]/div[3]/div')  # or driver.find_element_by_class_name('inner-div')

                    # Get the height of the browser window
                    window_height = driver.execute_script('return window.innerHeight;')

                    # Get the initial height of the inner div
                    inner_div_height = inner_div.size['height']

                    # Scroll down until the bottom of the inner div is visible
                    while driver.execute_script('return window.scrollY + arguments[0] < arguments[1];', window_height, inner_div_height):
                        driver.execute_script('window.scrollBy(0, arguments[0]);', 40)
                        time.sleep(1)
                    block.click()
        except:
            return()

def soup(id):
    row = {}
    attributes = ["Shooting range ID", "name", "is-member", "address", "address1", "phone", "email", "list-unstyled facility-details-list", "list-unstyled services-list", "list-unstyled shooting-av-list", "list-unstyled distance-list", "list-unstyled competitions-available-list"]
    soup = BeautifulSoup(driver.page_source,'lxml')
    attributes = soup.find("div", {"id": id})
    item_summary = attributes.find("div", {"class" : "location-item-summary"}).find("table", {'class' : 'table'})
    item_detail = attributes.find("div", {"class" : "location-item-details"})

    #range id
    rangeId = item_detail.find("span", {'class': 'id'}).text.strip()

    #check if the shooting range is already on chart
    if rangeId in unique_ids:
        return()
    unique_ids.add(rangeId)
    row['Shooting range ID'] = rangeId

    #name
    name = item_summary.find("h5", {'class': 'name'}).text.strip()
    row['Name'] = name

    #street
    street = item_summary.find("p", {'class' : 'address'}).text.strip() 
    row['Street address'] = street

    #state
    adrs = [x.strip() for x in item_summary.find("p", {'class' : 'address1'}).text.strip().split(",")]
    state = adrs[1]

    #check if shooting range in the states of California of Texas
    if (state != 'CA' and state != 'TX'):
        return()
    row['State'] = state

    #city
    city = adrs[0]
    row['City'] = city

    #zip code
    zipCode = adrs[2]
    row['Zip code'] = zipCode 

    #phone_number
    phone_number = item_summary.find("p", {'class' : 'phone'}).text.strip()
    row['Phone number'] = phone_number

    #nssf member
    nssf_member_span = item_summary.find('span', {'class': 'is-member'})
    if nssf_member_span:
        if nssf_member_span.get('style') == 'display: none;':
            nssf_member = 'Non-NSSF'
        else:
            nssf_member = nssf_member_span.text.strip()
    else:
        nssf_member = ''
    row['NSSF Member'] = nssf_member

    #facility_details
    facility_details = []
    ablbl = item_detail.find('ul', {'class': 'list-unstyled facility-details-list'}).find_all('li')
    unablbl = item_detail.find('ul', {'class': 'list-unstyled facility-details-list'}).find_all('li', {'class': 'hidden'})
    for facility in ablbl:
        if facility not in unablbl:
            facility_details.append(facility.text.strip())
    row['Facility Details'] = facility_details

    #services
    services = []
    ablbl = item_detail.find('ul', {'class': 'list-unstyled services-list'}).find_all('li')
    unablbl = item_detail.find('ul', {'class': 'list-unstyled services-list'}).find_all('li', {'class': 'hidden'})
    for service in ablbl:
        if service not in unablbl:
            services.append(service.text.strip())
    row['Services'] = services

    #shooting_available
    shooting_available = []
    ablbl = item_detail.find('ul', {'class': 'list-unstyled shooting-av-list'}).find_all('li')
    unablbl = item_detail.find('ul', {'class': 'list-unstyled shooting-av-list'}).find_all('li', {'class': 'hidden'})          
    shotgun = item_detail.find('ul', {'class': 'list-unstyled shooting-av-list'}).select('li[style*="display: none;"]')
    for av in ablbl:
        if av not in unablbl:
            shooting_available.append(av.text.strip())
    # Inconsistancy exists: element is hidden by display:none unlike others using class=hidden
    if len(shotgun) != 0:
        shooting_available.remove('Shotguns')
    row['Shooting Available'] = shooting_available
    
        
    #distances
    distance = []
    ablbl = item_detail.find('ul', {'class': 'list-unstyled distance-list'}).find_all('li')
    unablbl = item_detail.find('ul', {'class': 'list-unstyled distance-list'}).find_all('li', {'class': 'hidden'})
    for dis in ablbl:
        if dis not in unablbl:
            distance.append(dis.text.strip())
    row['Distance'] = distance

    #competitions
    competition = []
    ablbl = item_detail.find('ul', {'class': 'list-unstyled competitions-available-list'}).find_all('li')
    unablbl = item_detail.find('ul', {'class': 'list-unstyled competitions-available-list'}).find_all('li', {'class': 'hidden'})
    for comp in ablbl:
        if comp not in unablbl:
            competition.append(comp.text.strip())
    row['Competition'] = competition

    #websites (if any)
    web = item_detail.find("a", {'class' : 'btn btn-website website'})
    website = web['href'] if web else ''
    row['Website'] = website

    print(row)
    rows.append(row)




#url of the website to be scraped
url = "https://www.wheretoshoot.org/"
wait_time=4
delay_time=0.1

# Set driver as a Chrome driver
driver = webdriver.Chrome("C./chromedriver")
action = ActionChains(driver)
# access the website
driver.get(url)
driver.maximize_window()

#click accept cookie button
coockie = driver.find_element(By.XPATH, '//*[@id="cookie_action_close_header"]')
coockie.click()


#wait for the page to be loaded
driver.implicitly_wait(wait_time)

dropdown = driver.find_element(By.XPATH, '//*[@id="dropdownMenu1"]')
dropdown.click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="miles"]/ul/li[6]/a')))
time.sleep(2)
driver.implicitly_wait(wait_time)
first_option = driver.find_element(By.XPATH, '//*[@id="miles"]/ul/li[6]/a')
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

with open('shooting_ranges.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)


