from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "This is the first page"

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    return redirect(url_for('result', lat=data['lat'], lon=data['lon']))

@app.route('/result')
def result():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    # Render a new page with the received data
    return f"This is the redirected page with received data: {lat}, {lon}, {city}"

if __name__ == '__main__':
    app.run(debug=True)