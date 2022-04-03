from flask import Markup
from datetime import datetime

BASE = 'static/icons/weather'

# https://joelmccune.com/python-dictionary-as-object/


class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(
                    x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val)
                        if isinstance(val, dict) else val)


def get_icon(name: str, is_night: bool):
    name = name.lower()
    """
    Get an SVG icon from the static/icons folder and return the flask Markup

    https://www.weatherapi.com/docs/weather_conditions.json
    """
    svg = None

    if name == "sunny" or name == "clear":
        if is_night:
            svg = open(f'{BASE}/moon.stars.fill.svg').read()
        else:
            svg = open(f'{BASE}/sun.max.fill.svg').read()
            svg = f'<span style="color:var(--yellow);">{svg}</span>'
    elif name == "partly cloudy":
        if is_night:
            svg = open(f'{BASE}/cloud.moon.fill.svg').read()
        else:
            svg = open(f'{BASE}/cloud.sun.fill.svg').read()
    elif name == "cloudy" or name == "overcast":
        svg = open(f'{BASE}/cloud.fill.svg').read()
    elif name == "mist" or name == "patchy rain possible" or ("drizzle" in name and "freezing" not in name) or name == "light rain shower":
        svg = open(f'{BASE}/cloud.drizzle.fill.svg').read()
    elif name == "patchy snow possible" or name == "patchy light snow" or name == "light snow" or name == "patchy moderate snow":
        svg = open(f'{BASE}/cloud.snow.fill.svg').read()
    elif name == "patchy sleet possible" or name == "patchy freezing drizzle possible" or name == "light sleet" or name == "moderate or heavy sleet":
        svg = open(f'{BASE}/cloud.sleet.fill.svg').read()
    elif name == "thundery outbreaks possible":
        if is_night:
            svg = open(f'{BASE}/cloud.moon.bolt.fill.svg').read()
        else:
            svg = open(f'{BASE}/cloud.bolt.fill.svg').read()
    elif name == "blowing snow":
        svg = open(f'{BASE}/wind.snow.svg').read()
    elif name == "blizzard" or name == "patchy heavy snow" or name == "heavy snow" or name == "light snow showers" or name == "moderate or heavy snow showers" or name == "patchy light snow with thunder" or name == "moderate or heavy snow with thunder":
        svg = open(f'{BASE}/snow.svg').read()
    elif name == "fog" or name == "freezing fog":
        svg = open(f'{BASE}/cloud.fog.fill.svg').read()
    elif ("light rain" in name and "thunder" not in name) or name == "light freezing rain":
        svg = open(f'{BASE}/cloud.rain.fill.svg').read()
    elif "moderate rain" in name or "heavy rain" in name or name == "moderate or heavy freezing rain" or name == "moderate or heavy rain" or name == "torrential rain shower":
        svg = open(f'{BASE}/cloud.heavyrain.fill.svg').read()
    elif "ice pellets" in name or name == "light sleet showers" or name == "moderate or heavy sleet showers":
        svg = open(f'{BASE}/cloud.hail.fill.svg').read()
    elif "rain" in name and "thunder" in name:
        svg = open(f'{BASE}/cloud.bolt.rain.fill.svg').read()
    else:
        if is_night:
            svg = open(f'{BASE}/moon.stars.fill.svg').read()
        else:
            svg = open(f'{BASE}/sun.max.fill.svg').read()
            svg = f'<span style="color:var(--yellow);">{svg}</span>'

    return Markup(svg)


def get_day(date: str):
    """
    Get day of the week from date

    Date format: yyyy-mm-dd
    """

    parsed = datetime.strptime(date, "%Y-%m-%d")
    now = datetime.now().date()

    if now == parsed.date():
        return "Today"
    else:
        return parsed.strftime("%A")


def is_before_now(time: str):
    """
    Check if a time is before now

    Format: yyyy-mm-dd hh:mm
    """
    parsed = datetime.strptime(time, "%Y-%m-%d %H:%M")
    now = datetime.now()

    if parsed.hour < now.hour:
        return True
    else:
        return False


def is_now(time: str):
    """
    Check if a time is now

    format: yyyy-mm-dd hh:mm
    """

    parsed = datetime.strptime(time, "%Y-%m-%d %H:%M")
    now = datetime.now()

    if parsed.hour == now.hour:
        return True
    else:
        return False


def is_clear(condition: str):
    """Determines if the input (current conditions) is clear or not clear"""
    condition = condition.lower()
    if "sun" in condition or "sunny" in condition or "partly cloudy" in condition:
        return True
    else:
        return False


def is_night(input_current, input_today_dawn, input_today_dusk, input_tomorrow_dawn, input_tomorrow_dusk):
    """Determines if the current time is after dusk and before dawn of the following day"""
    current = datetime.strptime(input_current, "%Y-%m-%d %H:%M")
    today_dawn = datetime.strptime(input_today_dawn, "%Y-%m-%d %H:%M")
    today_dusk = datetime.strptime(input_today_dusk, "%Y-%m-%d %H:%M")
    tomorrow_dawn = datetime.strptime(input_tomorrow_dawn, "%Y-%m-%d %H:%M")
    tomorrow_dusk = datetime.strptime(input_tomorrow_dusk, "%Y-%m-%d %H:%M")

    # print(f'Current Day: {current.strftime("%Y-%m-%d")}, Today_dusk: {today_dusk.strftime("%Y-%m-%d")}, Today dawn: {today_dawn.strftime("%Y-%m-%d")}, Tomorrow dusk: {tomorrow_dusk.strftime("%Y-%m-%d")}, Tomorrow dawn: {tomorrow_dawn.strftime("%Y-%m-%d")}')

    if current.day == today_dusk.day and (current.hour > today_dusk.hour or (current.hour == today_dusk.hour and current.minute > today_dusk.minute)):
        return True
    elif current.day == today_dawn.day and (current.hour < today_dawn.hour or (current.hour == today_dawn.hour and current.minute < today_dawn.minute)):
        return True
    elif current.day == tomorrow_dusk.day and (current.hour > tomorrow_dusk.hour or (current.hour == tomorrow_dusk.hour and current.minute > tomorrow_dusk.minute)):
        return True
    elif current.day == tomorrow_dawn.day and (current.hour < tomorrow_dawn.hour or (current.hour == tomorrow_dawn.hour and current.minute < tomorrow_dawn.minute)):
        return True
    else:
        return False


def format_hour_forecast_obj(hour, today_sunrise, today_sunset, tomorrow_sunrise, tomorrow_sunset):
    temp_dict = {}

    if is_now(hour.time):
         temp_dict['time'] = "Now"
    else:
         temp_dict['time'] = Markup(datetime.strptime(hour.time, "%Y-%m-%d %H:%M").strftime("%-I<span class=\"small\">%p</span>"))

    hour_is_night = is_night(hour.time, today_sunrise, today_sunset, tomorrow_sunrise, tomorrow_sunset)
    temp_dict['icon'] = get_icon(hour.condition.text, hour_is_night)
    temp_dict['detail'] = round(hour.temp_f)
    return temp_dict