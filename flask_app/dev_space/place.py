import os
from dotenv import load_dotenv
from os.path import join, dirname
import googlemaps
import time
import re


try:
    dotenv_path = join(dirname(os.path.abspath(__file__)), './G_API_key.env')
    load_dotenv(dotenv_path, override=True)
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    print("get key successfully")
except:
    print("get key fail")
    exit()

gmaps_key = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)

def city_mapping(addr):
    geocode = gmaps_key.geocode(addr)
    loc = geocode[0]['geometry']['location']

    return loc

def city_keyword_mapping(specific_addr, keyword, radius_meter):
    place_results = {}
    if not isinstance(specific_addr, list):
        specific_addr = specific_addr.split(',')
    
    for addr in specific_addr:
        loc = city_mapping(addr)
        places = gmaps_key.places_nearby(
            keyword=keyword, location=loc, radius=radius_meter, language='zh-TW')
        
    while places:
        for place_item in places['results']:
            try:
                if re.search(keyword, place_item['name']) and place_item['vicinity']:
                    city_str = place_item['plus_code']['compound_code'][-3:]
                    place_results[place_item['name']] = city_str + place_item['vicinity']
                
                if re.search(keyword, place_item['name']) and not place_item['vicinity']:
                    place_results[place_item['name']] = city_str + place_item['formatted_address']
            except:
                print("Grab address error, exit the program!")
                exit()

        if 'next_page_token' in places:
            time.sleep(2)
            places = gmaps_key.places_nearby(page_token=places['next_page_token'])
        else:
            break
    print(place_results)
    return place_results

if __name__ == '__main__':
    # Use Specific address to find particular place
    # Want to find muti address, please use loop

    specific_addr = ["台北市大安區"]
    keyword = "麥當勞"
    radius_meter = 1000
    city_keyword_mapping(specific_addr, keyword, radius_meter)