import os
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

env_openw_api_key=os.environ.get("OPENWEATHER_API_KEY")
env_city_name=os.environ.get("CITY_NAME")

owm = OWM(env_openw_api_key)
mgr = owm.weather_manager()

observation = mgr.weather_at_place(env_city_name)
w = observation.weather

w.detailed_status         # e.g. 'clouds'
w.wind()                  # e.g. {'speed': 4.6, 'deg': 330}
w.humidity                # e.g. 87
w.temperature('celsius')  # e.g. {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
w.rain                    # e.g. {}
w.heat_index              # e.g. None
w.clouds                  # e.g. 75

str_temp = str(w.temperature('celsius')['temp'])
str_city = "\"" + env_city_name + "\""
str_des = "\"" + w.detailed_status  + "\""

print("source=openweathermap, city=" + str_city + ", description=" + str_des + ", temp=" + str_temp + ", humidity=" + str(w.humidity)) 
# e.g. source=openweathermap, city="Honolulu", description="few clouds", temp=70.2, humidity=75