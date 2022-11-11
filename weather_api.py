import os
import requests
import datetime
from pprint import pprint

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

def weather_city(city):
  try:
    print(city, "<---  city gotten")
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric")
    data = r.json()
    location = data["name"]
    temp = data["main"]["temp"]
    wind = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    day_length = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    return location, temp, wind, humidity, sunrise_time, sunset_time, day_length
  except Exception as ex:
    print(ex, "exception occured")