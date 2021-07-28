from flask import Flask


app = Flask(__name__)


from api_project import search_place
from api_project import region_weather