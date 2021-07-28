from flask import Flask, request, jsonify
import requests as rq
from bs4 import BeautifulSoup
import ast
import re
from datetime import datetime
from api_project import app


current_time = datetime.now()

@app.route('/weather/region', methods = ['GET'])
def r_weather():
    '''
    Use crawler to grab City's region prediction weather.
    url example: http://13.231.176.185:80/weather/region?city=64&region=6400100
    methods: GET
    return {
        'Time':['03 07/14', '06 07/14', ...],
        'C':{'T':[29, 28, ...], 'AT':[33, 33, ...]},
        'Wx':['多雲', '多雲', ...],
        'RH':['0%', '0%', ...],
        'Humidity':['80%', '76%', ...],
        'Comfort':['舒適', '舒適', ...]
        }
    '''
    # return data format
    result_dict = {
        'Time':[],
        'C':{'T':[], 'AT':[]},
        'Wx':[],
        'RH':[],
        'Humidity':[],
        'Comfort':[]
        }

    # Use GET methods to get variable
    city = request.args.get('city')
    region = request.args.get('region')

    rainh_list = list()
    Humidity_list = list()
    Comfort_list = list()

    weather = rq.get(
                "https://www.cwb.gov.tw/Data/js/3hr/ChartData_3hr_T_{}.js?T=2021070522-1&_=1625494733283".format(city))
    other_weather_data = rq.get(
                "https://www.cwb.gov.tw/V8/C/W/Town/MOD/3hr/{}_3hr_PC.html?T=2021070522-5".format(region))
    
    crawler_data = BeautifulSoup(other_weather_data.text, 'html.parser').find_all("tr")
    title_list = ['降雨機率','相對濕度','舒適度']

    for item in crawler_data:
        title = list(item.children)
        # 降雨機率, 放進result_dict
        [rainh_list.append(title[_item].text) for _item in range(3, len(title), 2) if title[1].text == title_list[0]]
        result_dict['RH'] = rainh_list
        # 相對濕度, 放進result_dict
        [Humidity_list.append(title[_item].text) for _item in range(3, len(title), 2) if title[1].text == title_list[1]]
        result_dict['Humidity'] = Humidity_list
        # 舒適度, 放進result_dict
        [Comfort_list.append(title[_item].text) for _item in range(3, len(title), 2) if title[1].text == title_list[2]]
        result_dict['Comfort'] = Comfort_list

    prediction_time_list = ast.literal_eval(
        re.search(r'(var Time_3hr) = (.*);', weather.text).group(2))
    prediction_weather = eval(
        re.search(r'(var TempArray_3hr) = ({.*)', weather.text, re.S).group(2).rstrip(';'))
    region_list = [item for item in prediction_weather]

    for value in prediction_weather.values():
        # 等API完成後會傳入region這個引數
        if region in region_list:
            temperature = value['C']['T']
            A_temperature = value['C']['AT']
            wx = [item[1] for item in value['Wx']['C']]
            result_dict['Time'] = prediction_time_list
            result_dict['C']['T'] = temperature
            result_dict['C']['AT'] = A_temperature
            result_dict['Wx'] = wx
            break
        else:
            return "Grab data wrong, please check your url or crawler url !!!"

    return result_dict

@app.route('/weather/city', methods = ['GET'])
def c_weather():
    '''
    Use crawler to grab City's current and prediction weather.
    url example: http://13.231.176.185:80/weather/city?city=64
    methods: GET
    '''
    city = request.args.get('city')
    weather = rq.get(
        "https://www.cwb.gov.tw/Data/js/TableData_36hr_County_C.js?T=202106{}{}".format(
            current_time.day, current_time.hour))

    city_weather = eval(
        re.search(r'({.*)', weather.text, re.S).group(0).rstrip(';'))
    city_list = [item for item in city_weather]

    if city in city_list:
        return jsonify(city_weather[city])
    else:
        return "Grab data wrong, please check your url or crawler url !!!"