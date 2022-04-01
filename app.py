import sys
import os
from flask import Flask, render_template, request, Markup
import urllib3
# from dotenv import dotenv_values
import json
from utils import DictObj, get_icon, get_day, is_before_now, is_now, is_clear
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

    # if request.method == "GET":

    #     ip_address = request.remote_addr

    #     # attempt to get the client's location from IP
    #     if ip_address != "127.0.0.1" and ip_address != None:
    #         try:
    #             req = requests.get(f'https://ipinfo.io/{ip_address}?token={env["IP_TOKEN"]}')  # noqa
    #             if req.status == 200:
    #                 data = req.json()
    #                 location = data['postal']
    #         except:
    #             print("Could not get location data from IP")
    #             # it will continue executing here, only with the default location (Boston)

    # else:
    #     # can be postal code or typed location
    #     location = request.form.get('location')

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
        for hour in hour_forecast:
            if is_before_now(hour.time):
                continue
            else:
                temp_dict = {}

                if is_now(hour.time):
                    temp_dict['time'] = "Now"
                else:
                    temp_dict['time'] = Markup(datetime.strptime(hour.time, "%Y-%m-%d %H:%M").strftime("%-I<span class=\"small\">%p</span>"))

                temp_dict['icon'] = get_icon(hour.condition.text)
                temp_dict['detail'] = round(hour.temp_f)
                forecast_list.append(temp_dict)

        # populate ten_day_forecast
        day_forecast = data.forecast.forecastday
        # TODO
        for day in day_forecast:
            temp_dict = {}
            temp_dict['time'] = get_day(day.date)
            temp_dict['icon'] = get_icon(day.day.condition.text)
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
