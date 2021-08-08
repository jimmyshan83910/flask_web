from flask import Flask

app = Flask(__name__)

from api_project import searchPlace
from api_project import region_weather
from api_project import place_vari_table