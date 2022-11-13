import os
import requests
from pprint import pprint

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

def forecast(city):
  try:
    location = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={WEATHER_API_KEY}")
    #r = requests.get(f"api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={WEATHER_API_KEY}")
    #data = r.json()
    pprint(location)
  except Exception as ex:
    print(ex, "exception occured")