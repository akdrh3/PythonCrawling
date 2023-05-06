import requests
from bs4 import BeautifulSoup
import csv

# define the URL for the search page
url = 'https://www.wheretoshoot.org/find-ranges/'

# define the search parameters (zip codes for California and Texas)
search_params = {
    'address': '',
    'state': '',
    'zipcode': 'CA, TX',
    'distance': '100'
}

# define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# send a GET request to the search page with the search parameters and headers
response = requests.get(url, params=search_params, headers=headers)

# parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# find all the shooting range listings on the search results page
range_listings = soup.find_all('div', {'class': 'list_item'})

# create a list to store the shooting range data
range_data = []

# loop through each shooting range listing
for range_listing in range_listings:

    # extract the shooting range ID
    range_id = range_listing.find('input', {'name': 'FormID'})['value']

    # extract the shooting range address, city, state, and zip code
    range_address = range_listing.find('div', {'class': 'address'}).text.strip()
    range_city = range_listing.find('div', {'class': 'city'}).text.strip()
    range_state = range_listing.find('div', {'class': 'state'}).text.strip()
    range_zip = range_listing.find('div', {'class': 'zip'}).text.strip()

    # extract the shooting range phone number
    range_phone = range_listing.find('div', {'class': 'phone'}).text.strip()

    # extract the NSSF Member vs. Non-NSSF Member status
    range_nssf_status = range_listing.find('div', {'class': 'member'}).text.strip()

    # extract the facility details
    range_facility_details = range_listing.find('div', {'class': 'facility_details'}).text.strip()

    # extract the shooting services available
    range_services = range_listing.find('div', {'class': 'services'}).text.strip()

    # extract the shooting options available
    range_shooting_available = range_listing.find('div', {'class': 'shooting'}).text.strip()

    # extract the distance to the shooting range
    range_distance = range_listing.find('div', {'class': 'distance'}).text.strip()

    # extract the competition information
    range_competition = range_listing.find('div', {'class': 'competition'}).text.strip()

    # extract the shooting range website (if any)
    range_website = range_listing.find('a', {'class': 'website_link'})
    if range_website is not None:
        range_website = range_website['href']
    else:
        range_website = ''

    # add the shooting range data to the list
    range_data.append([range_id, range_address, range_state, range_city, range_zip, range_phone, range_nssf_status,
                       range_facility_details, range_services, range_shooting_available, range_distance,
                       range_competition, range_website])

# deduplicate the shooting range data
deduplicated_range_data = [list(t) for t in {tuple(row) for row in range_data}]


