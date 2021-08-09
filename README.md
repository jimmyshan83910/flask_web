Jimmy的小小專案  
(nginx + uwsgi)
====
Flask api:
-------
1. flask_web/flask_app/api_project/search_place.py(已完成) 
#
    Url: http://13.231.176.185:80/meal  
    Methods: POST  
    Header = {Content-Type:application/json}  
    Body raw = {"specific_addr":"台北市大安區xx路xx號...","keyword":"麥當勞","radius_meter":"1000"} 
-------
2. flask_web/flask_app/api_project/region_weather.py
#
    a. 抓取縣市天氣  
        url: http://13.231.176.185:80/weather/city?city=64  
        methods: GET  
        參數表api: http://13.231.176.185:80/place_table?city=64
    
    b. 抓取地區天氣  
        url: http://13.231.176.185:80/weather/region?city=64&region=6400100  
        methods: GET  
        參數表api: http://13.231.176.185:80/place_table?city=64&region=6400100
