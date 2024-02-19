import sys
import time
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
POLLING_FREQ = int(os.getenv('POLLING_FREQ', 10))
ENTITIES_PER_ITERATION = int(os.getenv('ENTITIES_PER_ITERATION', 10))
API_GIS_BASE_URL = os.getenv('API_GIS_BASE_URL', 'http://api-gis:8080')
NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org/search'

# Functions
def fetch_countries_without_coordinates(limit):
    url = f"{API_GIS_BASE_URL}/countries_without_coordinates"
    params = {'limit': limit}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching countries: {response.status_code}, {response.text}")
        return []

def fetch_coordinates_for_country(country_name):
    params = {'q': country_name, 'format': 'json', 'limit': 1}
    response = requests.get(NOMINATIM_BASE_URL, params=params)
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        lat, lon = result['lat'], result['lon']
        logging.info(f"Fetched coordinates for {country_name}: Latitude {lat}, Longitude {lon}")
        return lat, lon
    else:
        logging.error(f"Error fetching coordinates for {country_name}: {response.status_code}, {response.text}")
        return None, None

def update_country_coordinates(country_id, country_name, lat, lon):
    url = f"{API_GIS_BASE_URL}/api/entities"
    data = {'country_id': country_id, 'latitude': lat, 'longitude': lon}
    response = requests.post(url, json=data)
    if response.status_code in [200, 201]:
        # Include the country's name in the log message
        logging.info(f"Coordinates updated for {country_name} (ID: {country_id}). Latitude: {lat}, Longitude: {lon}")
    else:
        logging.error(f"Failed to update coordinates for {country_name} (ID: {country_id}): {response.status_code}, {response.text}")

# Main Loop
if __name__ == "__main__":
    while True:
        countries = fetch_countries_without_coordinates(ENTITIES_PER_ITERATION)
        if countries:
            logging.info(f"Found {len(countries)} countries without coordinates.")
            for country in countries:
                lat, lon = fetch_coordinates_for_country(country['name'])
                if lat and lon:
                    # Pass the country's name to the update function
                    update_country_coordinates(country['id'], country['name'], lat, lon)
                else:
                    logging.error(f"Could not retrieve coordinates for {country['name']}")
        else:
            logging.info("No countries found that need coordinates updated.")
        time.sleep(POLLING_FREQ)
