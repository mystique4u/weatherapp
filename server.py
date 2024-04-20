from flask import Flask, render_template, request
import requests

# Other modules
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

app = Flask(__name__)

def get_weather(city):
    api_key = os.getenv("WAPI_KEY") # Replace with your API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        city_name = data['name']
        temperature = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        return {'city_name': city_name, 'temperature': temperature, 'weather_desc': weather_desc}
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
