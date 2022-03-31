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


def get_icon(name: str):
    name = name.lower()
    """
    Get an SVG icon from the static/icons folder and return the flask Markup

    https://www.weatherapi.com/docs/weather_conditions.json
    """
    svg = None

    if name == "sunny":
        svg = open(f'{BASE}/sun.max.fill.svg').read()
    elif name == "partly cloudy":
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
        svg = open(f'{BASE}/cloud.sun.fill.svg').read()

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