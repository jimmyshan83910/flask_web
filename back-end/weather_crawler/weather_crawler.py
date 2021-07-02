import requests as rq
from bs4 import BeautifulSoup
import json
from datetime import datetime
import chardet
import re
import psycopg2
from psycopg2.extras from RealDictCursor


class WeatherUpdate():
    def __init__(self):
        self.conn = psycopg2.connect(
            database = "jimmy_web", user = "postgres", password = "j3598418",
            host = "j-side-project.crv0ozn3ercx.ap-northeast-1.rds.amazonaws.com",
            port = "5432")

        self.db_weather = self.conn.cursor(cursor_factory = RealDictCursor)

    def grab_weather(self):
        on_the_hour = datetime.now()
        my_headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

        weather = rq.get(
            "https://www.cwb.gov.tw/Data/js/TableData_36hr_County_C.js?T=202106{}{}".format(
                on_the_hour.day, on_the_hour.hour),
                my_headers)

        extract_Kaohsiung_weather = eval(
            re.search(r'({.*)', weather.text, re.S).group(0).rstrip(';'))['64']

        # Insert database column
        for item in extract_Kaohsiung_weather:
            time_start = item['TimeRange'].split(' ~ ')[0]
            time_end = item['TimeRange'].split(' ~ ')[1]
            insert_db = "INSERT INTO weather.k_weather VALUES({}, {}, {}, {}, {}, {}, {})".format(
                time_start, time_end, item['Type']['C']['L'],
                item['Type']['C']['H'], item['PoP'], item['Wx'], item['CI'])

            conn_db = self.db_weather
            conn_db.execute(insert_db)
        # insert into time_start, time_end, temp_c_l, temp_c_h, pop, wx, ci

