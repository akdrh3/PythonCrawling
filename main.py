import requests
import csv
from bs4 import BeautifulSoup

# URL of the website to be scraped
url = "https://www.wheretoshoot.org/"

# Zip codes to search for shooting ranges in California and Texas
ca_zip_codes = [90001, 90210, 94102, 95111, 95814]  # Example zip codes for California
tx_zip_codes = [75001, 75201, 77001, 78701, 79901]  # Example zip codes for Texas

# Set up a CSV file to save the extracted data
field_names = ['Shooting Range ID', 'Street Address', 'City', 'State', 'Zip Code', 'Phone Number',
               'NSSF Membership', 'Facility Details', 'Services', 'Shooting Available', 'Distance',
               'Competition', 'Website']
csv_file = open('shooting_ranges.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(csv_file, fieldnames=field_names)
writer.writeheader()

# Function to scrape data for a given shooting range
def scrape_range_data(range):
    # Get the Form ID for the shooting range
    form_id = range.get('formnumber')

    # Get the address details for the shooting range
    address_details = range.find('div', class_='result-address')
    street_address = address_details.find('span', class_='street-address').text.strip()
    city = address_details.find('span', class_='locality').text.strip()
    state = address_details.find('span', class_='region').text.strip()
    zip_code = address_details.find('span', class_='postal-code').text.strip()

    # Get the phone number for the shooting range
    phone = range.find('div', class_='result-phone').text.strip()

    # Get the NSSF membership details for the shooting range
    nssf_member = range.find('div', class_='is-member').text.strip()

    # Get the facility details for the shooting range
    facility_details = range.find('div', class_='result-facility')
    facility = facility_details.find('span', class_='facility').text.strip()

    # Get the services offered by the shooting range
    services = range.find('div', class_='result-services').text.strip()

    # Get the shooting options available at the shooting range
    shooting_available = range.find('div', class_='result-shooting').text.strip()

    # Get the distance of the shooting range from the user's location
    distance = range.find('div', class_='result-distance').text.strip()

    # Get the competition details for the shooting range
    competition = range.find('div', class_='result-competition').text.strip()

    # Get the website URL for the shooting range
    website = range.find('div', class_='result-website').find('a')['href']

    # Create a dictionary with the extracted data
    range_data = {
        'Shooting Range ID': form_id,
        'Street Address': street_address,
        'City': city,
        'State': state,
        'Zip Code': zip_code,
        'Phone Number': phone,
        'NSSF Membership': nssf_member,
        'Facility Details': facility,
        'Services': services,
        'Shooting Available': shooting_available,
        'Distance': distance,
        'Competition': competition,
        'Website': website
    }

    return range_data

# Loop through each zip code in California and Texas and scrape shooting ranges in those
