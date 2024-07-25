import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def check_coordinates(latitude, longitude):
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180.")

def convert_location(latitude, longitude):
    api_key = ''
    url = 'http://api.openweathermap.org/geo/1.0/reverse'
    params = {'lat': latitude, 'lon': longitude, 'appid': api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            city = data[0].get('name', '')
            country = data[0].get('country', '')
            location = city + "," + country
            return location
        else:
            return "Location not found"
    else:
        return f"Error: {response.status_code}"

def get_weather(latitude, longitude, location):
    api_key = ''
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'lat': latitude, 'lon': longitude, 'appid': api_key, 'units': 'metric'}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = {
            'time': data['dt'], 
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'location': location
        }
        return weather
    else:
        return f"Error: {response.status_code}"


@app.route('/weather', methods=['GET','POST'])

def show_weather():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lon'))

    check_coordinates(latitude, longitude)
    location = convert_location(latitude, longitude)
    weather = get_weather(latitude, longitude, location)

    return jsonify(weather)


if __name__ == '__main__':  
   app.run(debug=True)