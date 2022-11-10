import os
import requests
from pprint import pprint

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

def weather_city(city):
  try:
    print(city, "<---  city gotten")
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}")
    data = r.json()
    pprint(data)
  except Exception as ex:
    print(ex, "exception occured")