from flask import Flask, request
from api_project import app
import json




@app.route('/place_table', methods=['GET'])
def grab_city_region_table():
    '''
    Let user get table of city and region variable
    url example: http://13.231.176.185:80/place_table?city=64
    url example 2: http://13.231.176.185:80/place_table?city=64&region=6400100
    methods: GET
    '''
    path = '/home/jimmyshan/work_space/flask_app/api_project/data/'

    city_id = request.args.get('city')
    region_id = request.args.get('region')
    if city_id and not region_id:
        with open(path + 'city_list.json', 'r') as file:
            result_list = json.load(file)

    if city_id and region_id:
        with open(path + 'region_list.json', 'r') as file:
            result_list = json.load(file)

    # 特別說明: 如果要有人性化的顯示，需等待我開發前端...
    return result_list