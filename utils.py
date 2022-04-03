from flask import Markup
from datetime import datetime, timedelta
import pendulum

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


def get_icon(name: str, is_night: bool, chance_of_rain: float, chance_of_snow: float):
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
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
    elif name == "patchy snow possible" or name == "patchy light snow" or name == "light snow" or name == "patchy moderate snow":
        svg = open(f'{BASE}/cloud.snow.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_snow)}%</span></span>'
    elif name == "patchy sleet possible" or name == "patchy freezing drizzle possible" or name == "light sleet" or name == "moderate or heavy sleet":
        svg = open(f'{BASE}/cloud.sleet.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
    elif name == "thundery outbreaks possible":
        chance = {'show': False, 'value': 0}
        if chance_of_rain > 0 or chance_of_snow > 0:
            chance_value = 0
            if chance_of_rain > 0:
                chance_value = chance_of_rain
            else:
                chance_value = chance_of_snow
            chance = {'show': True, 'value': chance_value}
        if is_night:
            svg = open(f'{BASE}/cloud.moon.bolt.fill.svg').read()
        else:
            svg = open(f'{BASE}/cloud.bolt.fill.svg').read()
        if chance['show']:
            svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance["value"])}%</span></span>'
    elif name == "blowing snow":
        svg = open(f'{BASE}/wind.snow.svg').read()
    elif name == "blizzard" or name == "patchy heavy snow" or name == "heavy snow" or name == "light snow showers" or name == "moderate or heavy snow showers" or name == "patchy light snow with thunder" or name == "moderate or heavy snow with thunder":
        svg = open(f'{BASE}/snow.svg').read()
    elif name == "fog" or name == "freezing fog":
        svg = open(f'{BASE}/cloud.fog.fill.svg').read()
    elif ("light rain" in name and "thunder" not in name) or name == "light freezing rain":
        svg = open(f'{BASE}/cloud.rain.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
    elif "moderate rain" in name or "heavy rain" in name or name == "moderate or heavy freezing rain" or name == "moderate or heavy rain" or name == "torrential rain shower":
        svg = open(f'{BASE}/cloud.heavyrain.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
    elif "ice pellets" in name or name == "light sleet showers" or name == "moderate or heavy sleet showers":
        svg = open(f'{BASE}/cloud.hail.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
    elif "rain" in name and "thunder" in name:
        svg = open(f'{BASE}/cloud.bolt.rain.fill.svg').read()
        svg = f'<span class="probability-icon">{svg}<span class="probability-value">{int(chance_of_rain)}%</span></span>'
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
        time = datetime.strptime(hour.time, "%Y-%m-%d %H:%M")
        temp_dict['time'] = Markup(time.strftime("%-I<span class=\"small\">%p</span>"))

    hour_is_night = is_night(hour.time, today_sunrise, today_sunset, tomorrow_sunrise, tomorrow_sunset)
    temp_dict['icon'] = get_icon(hour.condition.text, hour_is_night, hour.chance_of_rain, hour.chance_of_snow)
    temp_dict['detail'] = round(hour.temp_f)
    return temp_dict

# https://stackoverflow.com/questions/46736529/how-to-compute-the-time-difference-between-two-time-zones-in-python
def tz_diff(home, away, on=None):
    """
    Return the difference in hours between the away time zone and home.

    `home` and `away` may be any values which pendulum parses as timezones.
    However, recommended use is to specify the full formal name.
    See https://gist.github.com/pamelafox/986163

    As not all time zones are separated by an integer number of hours, this
    function returns a float.

    As time zones are political entities, their definitions can change over time.
    This is complicated by the fact that daylight savings time does not start
    and end on the same days uniformly across the globe. This means that there are
    certain days of the year when the returned value between `Europe/Berlin` and
    `America/New_York` is _not_ `6.0`.

    By default, this function always assumes that you want the current
    definition. If you prefer to specify, set `on` to the date of your choice.
    It should be a `Pendulum` object.

    This function returns the number of hours which must be added to the home time
    in order to get the away time. For example,
    ```python
    >>> tz_diff('Europe/Berlin', 'America/New_York')
    -6.0
    >>> tz_diff('Europe/Berlin', 'Asia/Kabul')
    2.5
    ```
    """
    if on is None:
        on = pendulum.today()
    diff = (on.timezone_(home) - on.timezone_(away)).total_hours()

    # what about the diff from Tokyo to Honolulu? Right now the result is -19.0
    # it should be 5.0; Honolulu is naturally east of Tokyo, just not so around
    # the date line
    if abs(diff) > 12.0:
        if diff < 0.0:
            diff += 24.0
        else:
            diff -= 24.0

    return diff