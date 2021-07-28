from flask import Flask


app = Flask(__name__)


from api_project import search_meal
from api_project import region_weather