from api_project.meal import app2
from api_project.region_weather import app_weather


from flask import Flask




app = Flask(__name__)

app.register_blueprint(app2)
app.register_blueprint(app_weather)