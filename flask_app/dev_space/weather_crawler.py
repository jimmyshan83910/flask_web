import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import time
from datetime import datetime
import requests as rq
import re
from config import database
import psycopg2
from psycopg2.extras import RealDictCursor
import ast
from bs4 import BeautifulSoup
from bs4 import NavigableString


class WeatherUpdate():
    def __init__(self):
        '''
        Define class variable about database and time
        '''
        self.conn = database.WeatherDB()
        self.conn.get_db()
        self.date = datetime.now()
        self.city_list = {}
        self.region_list = {}

    def region_prediction_weather(self, city="64", region="6400100"):
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
        # city = request.args.get('city')
        # region = request.args.get('region')

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
            re.search(r'(var TempArray_3hr) = ({.*);', weather.text, re.S).group(2))
        region_list = [item for item in prediction_weather]

        for value in prediction_weather.values():
            if region in region_list:
                temperature = value['C']['T']
                A_temperature = value['C']['AT']
                wx = [item[1] for item in value['Wx']['C']]
                # 天氣預報時間表, 放進result_dict
                result_dict['Time'] = prediction_time_list
                # 攝氏溫度, 放進result_dict
                result_dict['C']['T'] = temperature
                # 攝氏體感溫度, 放進result_dict
                result_dict['C']['AT'] = A_temperature
                # 天氣情況, 放進result_dict
                result_dict['Wx'] = wx
                break
            else:
                return "Grab data wrong, please check your url or crawler url !!!"

        # return result_dict
        print(result_dict)

    def region_current_weather(self):
        '''
        Use crawler to grab City's region current weather.
        Doesn't finish yet, this founction will connect API.
        '''
        weather = rq.get(
                    "https://www.cwb.gov.tw/Data/js/GT/TableData_GT_T_64.js?T=2021070518-2&_=1625480972142")
        current_weather = eval(re.search(r'(var GT) = ({.*);', weather.text, re.S).group(2))

        for key, value in current_weather.items():
            print(key)
            input(value)

    def city_weather(self, city="64"):
        '''
            Use crawler to grab City's current and prediction weather.
            url example: http://13.231.176.185:80/c_weather?city=64
        '''
        weather = rq.get(
            "https://www.cwb.gov.tw/Data/js/TableData_36hr_County_C.js?T=202106{}{}".format(
                self.date.day, self.date.hour))

        city_weather = eval(re.search(r'({.*);', weather.text, re.S).group(0))
        
        # return city_weather[city]
        print(city_weather[city])

        # # Insert database column
        # for item in extract_Kaohsiung_weather:
        #     combine_sta = (item['TimeRange'].split(' ~ ')[0].split('-')[0].replace('/', '-')
        #                     + " " + item['TimeRange'].split(' ~ ')[0].split('-')[1]) + ":00"
        #     combine_end = (item['TimeRange'].split(' ~ ')[1].split('-')[0].replace('/', '-')
        #                     + " " + item['TimeRange'].split(' ~ ')[1].split('-')[1]) + ":00"

        #     time_start = str(self.date.year) + "-" + combine_sta
        #     time_end = str(self.date.year) + "-" + combine_end

        #     insert_db = "INSERT INTO weather.k_weather VALUES(%s, %s, %s, %s, %s, %s, %s)"
        #     values = [
        #         time_start, time_end, item['Temp']['C']['L'], item['Temp']['C']['H'],
        #         item['PoP'], item['Wx'], item['CI']]

        #     self.db_weather.execute(insert_db, values)

        # self.db_weather.close()
        # self.conn.close()

if __name__ == '__main__':
    weather_class = WeatherUpdate()

    weather_class.region_prediction_weather()
    # weather_class.region_current_weather()
    # weather_class.city_weather()