import requests as rq
from datetime import datetime
import re
import psycopg2
from psycopg2.extras import RealDictCursor
import time


class WeatherUpdate():
    def __init__(self):
        self.conn = psycopg2.connect(
            database = "jimmy_web", user = "postgres", password = "j3598418",
            host = "j-side-project.crv0ozn3ercx.ap-northeast-1.rds.amazonaws.com",
            port = "5432")
        self.conn.set_session(autocommit=True)
        self.date = datetime.now()
        self.db_weather = self.conn.cursor(cursor_factory = RealDictCursor)

    def grab_weather(self):
        my_headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

        weather = rq.get(
            "https://www.cwb.gov.tw/Data/js/TableData_36hr_County_C.js?T=202106{}{}".format(
                self.date.day, self.date.hour),
                my_headers)

        extract_Kaohsiung_weather = eval(
            re.search(r'({.*)', weather.text, re.S).group(0).rstrip(';'))['64']

        # Insert database column
        for item in extract_Kaohsiung_weather:
            combine_sta = (item['TimeRange'].split(' ~ ')[0].split('-')[0].replace('/', '-')
                           + " " + item['TimeRange'].split(' ~ ')[0].split('-')[1]) + ":00"
            combine_end = (item['TimeRange'].split(' ~ ')[1].split('-')[0].replace('/', '-')
                           + " " + item['TimeRange'].split(' ~ ')[1].split('-')[1]) + ":00"

            time_start = str(self.date.year) + "-" + combine_sta
            time_end = str(self.date.year) + "-" + combine_end

            insert_db = "INSERT INTO weather.k_weather VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = [
                time_start, time_end, item['Temp']['C']['L'], item['Temp']['C']['H'],
                item['PoP'], item['Wx'], item['CI']]

            self.db_weather.execute(insert_db, values)

        self.db_weather.close()
        self.conn.close()

if __name__ == '__main__':
    while True:
        current_ts = datetime.now()
        print(current_ts)
        if (current_ts.hour == 15 and current_ts.minute == 52):
            # Crawler weather data and insert into DB
            WeatherUpdate().grab_weather()
            print("Processing data done, Wait 23 hours for next process")
            time.sleep(82800)
        else:
            print("System sleep")
            time.sleep(3)