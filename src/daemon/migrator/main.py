import psycopg2
import xml.etree.ElementTree as ET
import os
import requests
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection parameters from environment variables
PG_XML_CONN_STR = os.getenv('PG_XML_CONN_STR')
PG_REL_CONN_STR = os.getenv('PG_REL_CONN_STR')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://api-entities:8080')

# ... [Previous code, including the imports and logging configuration] ...

def post_country(country_name):
    url = f"{API_BASE_URL}/countries"
    data = {"name": country_name}
    response = requests.post(url, json=data)
    return response

# ... [Other functions: get_countries, delete_country, update_country] ...

def fetch_xml_parts():
    parts = []
    with psycopg2.connect(PG_XML_CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, xml_part FROM converted_documents WHERE is_processed = FALSE")
            parts = cur.fetchall()
    return parts

def mark_xml_part_processed(part_id):
    with psycopg2.connect(PG_XML_CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE converted_documents SET is_processed = TRUE WHERE id = %s", (part_id,))
        conn.commit()

def parse_countries_from_xml(xml_part):
    root = ET.fromstring(xml_part)
    country_elements = root.findall('.//Countries/Country')
    return [elem.get('country') for elem in country_elements]

def insert_countries(countries):
    with psycopg2.connect(PG_REL_CONN_STR) as conn:
        with conn.cursor() as cur:
            for country_name in countries:
                if country_name:  
                    cur.execute("INSERT INTO Countries (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (country_name,))
        conn.commit()

def process_xml_part(part_id, xml_part):
    countries = parse_countries_from_xml(xml_part)
    if countries:
        for country_name in countries:
            if country_name: 
                response = post_country(country_name)
                if response.status_code in [200, 201]:
                    logging.info(f"Country {country_name} added successfully.")
                else:
                    logging.error(f"Failed to add country {country_name}: {response.status_code}, {response.text}")
    else:
        logging.info(f"No countries found in part {part_id}. Marking as processed.")
    mark_xml_part_processed(part_id)

def main():
    while True: 
        xml_parts = fetch_xml_parts()
        if not xml_parts:
            logging.info("No new XML parts found. Waiting...")
            time.sleep(30) 
            continue

        for part_id, xml_part in xml_parts:
            process_xml_part(part_id, xml_part)

        logging.info("Processed current batch of XML parts. Waiting...")
        time.sleep(30)  

if __name__ == "__main__":
    main()
