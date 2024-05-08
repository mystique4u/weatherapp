from flask import Flask, render_template, request
import requests

# Other modules
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("WAPI_KEY") # Replace with your API key

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        city_name = data['name']
        country_name = data['sys']['country']
        temperature = round(data['main']['temp'])
        weather_desc = data['weather'][0]['description']
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        weather_icon = data['weather'][0]['icon']

        return {'city_name': city_name, 'country_name': country_name, 'temperature': temperature, 'weather_desc': weather_desc, 'lon': lon, 'lat': lat, 'weather_icon': weather_icon}
    else:
        return None

def get_forecast(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=5&appid={api_key}'
    lat = get_weather(lat)
    lon = get_weather(lon)
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # extract the data
        day_of_week = data['list'][0]['dt']
        icon = data['list'][1]['weather'][1]['icon']
        description = data['list'][1]['weather'][1]['description']

        return {'day_of_week': day_of_week, 'icon': icon, 'description': description}
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('result.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
