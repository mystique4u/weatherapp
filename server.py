from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime


# Other modules
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("WAPI_KEY") # Replace with your API key


def get_weather(**key):
    if 'city' in key:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={key['city']}&appid={api_key}&units=metric'
    else:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={key['lat']}&lon={key['lon']}&appid={api_key}&units=metric'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        country_name = data['sys']['country']
        temperature = round(data['main']['temp'])
        weather_desc = data['weather'][0]['description']
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        weather_icon = data['weather'][0]['icon']

        return {'city_name': city_name, 
                'country_name': country_name, 
                'temperature': temperature, 
                'weather_desc': weather_desc, 
                'lon': lon, 
                'lat': lat, 
                'weather_icon': weather_icon
                }
    else:
        return None

def get_forecast(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        # extract the data
        forecast_array = []
        for obj in data['list']:
            dt_txt_arr = obj['dt_txt'].split(' ')
            if dt_txt_arr[1] == '12:00:00': #data filter
                dt_object = datetime.datetime.fromtimestamp(obj['dt'])
                item = {
                    'day': dt_object.strftime("%A")[: 3],
                    'icon': obj['weather'][0]['icon'],
                    'description': obj['weather'][0]['description'],
                    'temperature': round(obj['main']['temp'])
                }
                forecast_array.append(item)
        return forecast_array
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    weather_data = None
    to_html_forecast_data = None

    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city = request.args.get('city')
    if request.method == 'GET':
        if city:
            weather_data = get_weather(city=city)
            if weather_data:
                lat = weather_data['lat']
                lon = weather_data['lon']
                to_html_forecast_data = get_forecast(lat, lon)
        else:
            weather_data = get_weather(lat=lat, lon=lon)
            if weather_data:
                lat = weather_data['lat']
                lon = weather_data['lon']
                to_html_forecast_data = get_forecast(lat, lon)

    return render_template('result.html', weather_data=weather_data, forecast_data = to_html_forecast_data )

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    if data:
        lat = data.get('latitude')
        lon = data.get('longitude')

        return redirect(url_for('result', lat=data['lat'], lon=data['lon']))
        # return city_name
    else:
        return ''

if __name__ == '__main__':
    app.run(debug=True)