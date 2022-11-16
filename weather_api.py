import os
import requests
import datetime
from pprint import pprint

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

weather_symbols = {
  "Snow": "\U0001F328",
  "Clouds": "\U00002601",
  "Rain": "\U00002614",
  "Drizzle": "\U00002614",
  "Thunderstorm": "\U000026A1",
  "Mist": "\U0001F32B",
  "Clear": "\U00002600",
  "Fog": "\U0001F32B"
}

# Weather data by city
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
    weather_symbol = data["weather"][0]["main"]
    return location, temp, wind, humidity, sunrise_time, sunset_time, day_length, weather_symbol
  except Exception as ex:
    print(ex, "exception occured")

# Print weather
def getWeather(text):
      symbol = ""
      city = text.replace("weather ", "")
      print("weather recognized -->", city)
      weather = weather_city(city)
      pprint(weather)
      if weather[7] in weather_symbols:
        symbol = weather_symbols[weather[7]]
      current_weather = f"Weather in {weather[0]}\nTemperature {weather[1]} °C\n{weather[7]} {symbol}\nWind speed {weather[2]} m/s\nHumidity {weather[3]}%\nSunrise {weather[4]}\nSunset {weather[5]}\nLength of day is {weather[6]}"
      return current_weather