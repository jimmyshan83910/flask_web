import json


with open('../api_project/data/city_list.json') as file:
    result_1 = json.load(file)

with open('../api_project/data/region_list.json') as file:
    result_2 = json.load(file)

print(result_2)