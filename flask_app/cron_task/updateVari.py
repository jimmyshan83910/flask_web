import re
import requests as rq
import json
from bs4 import BeautifulSoup
import ast
from collections import defaultdict


def grab_city_list():
    ## I need to learn how to crawler about JS or Http header usage in web  
    # data = web_crawler()
    data = rq.get(
        "https://www.cwb.gov.tw/Data/js/info/Info_County.js?v=20200415")
    
    soup = BeautifulSoup(data.text, 'lxml')
    city = ast.literal_eval(
        re.search(r'(var Info_County) = (.*);', soup.text, re.S).group(2))

    city_dict = {item['ID']:item['Name']['C']
        for item in city if item['ID'] and item['Name']['C']}

    with open('../api_project/data/city_list.json', 'w') as file:
        json.dump(city_dict, file)
    
    print("city_list.json done!!!")

def grab_region_list():
    data = rq.get(
        "https://www.cwb.gov.tw/Data/js/info/Info_Town.js?v=20200817")
    
    soup = BeautifulSoup(data.text, 'lxml')

    region_dict = re.search(r'(var Info_Town) = (.*);', soup.text, re.S).group(2)
    region_dict = eval(
        region_dict.replace("true", '''"true"''').replace("false", '''"false"'''))

    result_dict = {}
    for key, value in region_dict.items():
        temp_list = list()
        for item in value:
            pop_key = ('RID', 'Tide')
            [item.pop(_key) for _key in pop_key]
            temp_list.append(item)
        
        result_dict[key] = temp_list
   
    with open('../api_project/data/region_list.json', 'w') as file:
        json.dump(result_dict, file)

    print("region_list.json done!!!")

if __name__ == "__main__":
    grab_city_list()
    grab_region_list()