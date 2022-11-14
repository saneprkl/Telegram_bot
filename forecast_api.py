import os
import requests
from pprint import pprint

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

def forecast(city):
  try:
    
    cityLocationRes = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={WEATHER_API_KEY}")
    locationData = cityLocationRes.json()
    lat = locationData[0]["lat"]
    long = locationData[0]["lon"]
    print(locationData, "found in forecast")
    
    r = requests.get(f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={long}&cnt={4}&appid={WEATHER_API_KEY}")
    data = r.json()
    pprint(data)
  except Exception as ex:
    print(ex, "exception occured")