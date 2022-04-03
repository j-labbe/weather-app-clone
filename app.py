import sys
import os
from flask import Flask, render_template, request, Markup
import urllib3
# from dotenv import dotenv_values
import json
from utils import DictObj, format_hour_forecast_obj, get_icon, get_day, is_before_now, is_now, is_clear, is_night, format_hour_forecast_obj
from datetime import datetime
import requests #type: ignore

# env = dotenv_values('.env')

# if not env['IP_TOKEN'] or env['IP_TOKEN'] == None:
#     print("IPInfo.io token is required!\n")
#     print("Create a .env file in the project root and set IP_TOKEN to your api token.")
#     sys.exit(1)

# if not env['WEATHER_API_KEY'] or env['WEATHER_API_KEY'] == None:
#     print("WeatherAPI.com API key is required!\n")
#     print("Create a .env file in the project root and set WEATHER_API_KEY to your api token.")
#     sys.exit(1)

http = urllib3.PoolManager()

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET', 'POST'])
def index():

    # default location
    location = '02108'

    if request.method == "POST":
        location = request.form.get('location')

    # get weather data
    try:
        req = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key=5c984dc01e53499d9d202112222403&q={location}&days=3&aqi=no&alerts=no")  # noqa
        data = DictObj(req.json())

        if hasattr(data, 'error') and (hasattr(data.error, 'code') and (data.error.code == 1006 or hasattr(data.error, 'message'))):
            print("Location error")
            return render_template("error.html", location=location, heading="Error", message=f"Could not get weather data for that location ({location}).")
        
        location_city_town = data.location.name
        temperature = round(data.current.temp_f)
        conditions = data.current.condition.text
        high_temp = round(data.forecast.forecastday[0].day.maxtemp_f)
        low_temp = round(data.forecast.forecastday[0].day.mintemp_f)
        forecast_list = [] # list of dicts
        ten_day_forecast = [] # list of dicts

        # populate forecast_list
        hour_forecast = data.forecast.forecastday[0].hour
        
        # get the sunrise/sunset times & conver to correct formats
        # add date & convert to 24 hour time
        now_date = data.location.localtime.split(" ")[0]
        tomorrow_date = data.forecast.forecastday[1].date
        today_sunrise    = now_date + " " + datetime.strptime(data.forecast.forecastday[0].astro.sunrise, "%I:%M %p").strftime("%H:%M")
        today_sunset     = now_date + " " + datetime.strptime(data.forecast.forecastday[0].astro.sunset,  "%I:%M %p").strftime("%H:%M")
        tomorrow_sunrise = tomorrow_date + " " + datetime.strptime(data.forecast.forecastday[1].astro.sunrise, "%I:%M %p").strftime("%H:%M")
        tomorrow_sunset  = tomorrow_date + " " + datetime.strptime(data.forecast.forecastday[1].astro.sunset,  "%I:%M %p").strftime("%H:%M")

        for hour in hour_forecast:
            # omit any weather data before the current hour
            if is_before_now(hour.time):
                continue
            else:
                forecast_item = format_hour_forecast_obj(hour, today_sunrise, today_sunset, tomorrow_sunrise, tomorrow_sunset)
                forecast_list.append(forecast_item)

        if len(forecast_list) < 24:
            hour_forecast = data.forecast.forecastday[1].hour
            for hour in hour_forecast:
                if len(forecast_list) < 24:
                    forecast_item = format_hour_forecast_obj(hour, today_sunrise, today_sunset, tomorrow_sunrise, tomorrow_sunset)
                    forecast_list.append(forecast_item)
                else:
                    break

        # populate ten_day_forecast
        day_forecast = data.forecast.forecastday
        # TODO
        for day in day_forecast:
            temp_dict = {}
            temp_dict['time'] = get_day(day.date)
            temp_dict['icon'] = get_icon(day.day.condition.text, False)
            temp_dict['low_temp'] = round(day.day.mintemp_f)
            temp_dict['high_temp'] = round(day.day.maxtemp_f)
            ten_day_forecast.append(temp_dict)

        # select the correct background for the current conditions
        condition_class = ""
        if is_clear(data.current.condition.text):
            condition_class = "bg-clear"
        else:
            condition_class = "bg-notclear"

        return render_template("output.html", location_city_town=location_city_town, temperature=temperature, conditions=conditions, high_temp=high_temp, low_temp=low_temp, forecast_list=forecast_list, ten_day_forecast=ten_day_forecast, condition_class=condition_class)
    except Exception as e:
        print(e)
        return render_template("error.html", location=location, heading="Error", message="Could not get weather data for that location.")
