# Apple Weather App Clone

This is a clone of the Apple Weather app that comes preinstalled on most iOS devices.

Fully operational at [this link!](http://weather.jacklabbe.com)
Code viewable [here on GitHub!](https://github.com/j-labbe/weather-app-clone)

This project is exactly what the title says it is: a clone of the Apple iOS Weather application. The code on GitHub is optimized for deployment on Heroku, but can easily be adapted to any PaaS of your choice.

## Features
A full list of features included (as of submission) are:
- Weather data for any location on Earth
- Dynamic UI changes based on weather conditions
    - Dynamic SVG icon rendering based on weather conditions
    - Extremely close UI design to iOS' official application
- Timezone optimization (weather will be accurate across timezones)
- Link sharing and URL parameters (ex: `http://weather.jacklabbe.com/?location=your_location_here`)
- and more!

## Technologies Used
- Flask
- [Public Weather API](http://weatherapi.com) (for weather data)
- [Public IP Address Location API](https://ipinfo.io) (for retrieving the zip code of the IP address that requested the content)

## Languages
- Python
- Jinja
- HTML
- CSS
- JavaScript (Pure)

## Challenges Faced
My previous web app experience has mostly been with vanilla JS or React. I wanted to try new and unfamiliar technologies to broaden my knowledge and experience. 

With that came many trips to the Flask docs, many searches on Stackoverflow, and much time spent in my debugger. 

Specific challenges included:
1. Jinja loops
2. Python `str` to `datetime` conversion
3. Dynamic `<body>` classes while using Flask's `render_template` function to render a component that extends the main layout

## Things that could be improved (or added)
1. Dynamic backgrounds
2. Colorize weather icons
3. 10-day forecast (this functionality required a subscription for the weather API)
4. Rewrite to support ajax calls to prevent entire page refreshes
5. User accounts (to save locations, just like on iOS)
6. High-low-avg graphs for daily forecasts

## Implementation Details

Specific details about files and directories in this project are as follows:

<br>

### `/static` - Static Assets
Includes:
- SFPro font
- client.js - Client-side JavaScript responsible for clock and search button handling
- styles.css - Complete styling for application

<br>

### `/static/icons` - SF Symbols
Directory that holds all symbols relevant to this project.

<br>

### `/templates` - HTML Templates
Directory that holds all templates used by the application.

<br>

### `/templates/error.html` - Error Template
Template responsible for displaying error messages a little bit prettier than default system error messages.
Parameters passed utilizing Flask's `render_template` function.

<br>

### `/templates/layout.html` - General Layout
Template that handles the general layout of the webpage.
Parameters passed utilizing Flask's `render_template` function.

#### Notable Elements:
- `block title` - Title of the webpage
- Meta tags - viewport
- `<script>` and `<link>` tags - JavaScript and CSS requirements.
- `block body_tag` - Holds __only__ the opening tag for the body.
    - This is done because it was the simplest way to be able to adjust the body class list.
- `block main` - Main output for application.
- `div footer` - Expanding footer section with search form.

<br>

### `/templates/output.html` - Application Output
Template that is rendered with all the output including weather data.

<br>

#### Notable Elements:
- `block title` - City/town included in site title
- `block body_tag` - class changes based on weather conditions (controls the color of the background).
- `div header` - Outputs the city/town name, the temperature, conditions, and the high and low for the current day.
- `div today-forecast` - Hourly forecast for the current day. Uses a jinja loop to create elements based on a list of dicts that hold a time, icon, and temperature in each dict.
- `div ten-day-forecast` - Daily forecasting (demo has three days because 10 days required a paid subscription to [API](http://weatherapi.com)).
    - Includes time, icon, high and low for each day
    - Outputs a vertical list of horizonal elements (where each element has time, temp, etc.)

<br>

### `.gitignore` - Gitignore

<br>

### `LICENSE` - License for project (MIT)

<br>

### `Procfile` - Heroku
Required for Heroku deployment. Tells the dyno what to do to run the app and what kind of service it is.
`gunicorn` is used to run the application after being compiled by Heroku's services.

<br>

### `runtime.txt` - Heroku
Tells dyno what version of Python to use.

<br>

### `requirements.txt` - Python requirements

<br>

### `app.py` - Main Flask application
First the app checks for an environment variable called production. If it's present, other environment variables are loaded from `os.environ`, otherwise it uses `.env` to load from a `.env` file in the project root (this makes development easier, since all one does it add a new var to the `.env`, instead of exporting and whatnot. Especially useful for changing variables quickly).

Next the application initializes the Flask application and disables caching.

One route is defined in this app, and is accepts both `GET` and `POST` methods.

The default location is `Boston, Massachusetts` in the `America/New_York` timezone.

Heroku forwards all traffic using a reverse-proxy, so the `X-Forwarded-For` header is supplied to allow the server to know which IP address requested content. If `X-Forwarded-For` is not present, IP tracking is skipped. IP info is supplied by `ipinfo.io`, which provides the Timezone for the client that requested the resource. If IP tracking is skipped, the default timezone is used.

Next the application checks for `?location` as a URL argument. This allows links to be shared with others, because if a location is provided the application sets that location as the location to get weather data for.

Before grabbing the weather data, the timezone is set on the server (because it affects how the API data is fetched. Without setting the timezone, incorrect times were calculated).

The application converts the response dict to an object to make things easier to type (see `utils.py`).

Fields are populated with data from the API, and properly formatted.

Two loops are used to build the list of dicts that will be interpreted by jinja.

The first builds the list for the hourly forecast. Each dict within the loop is created via `format_hour_forecast_obj` (see `utils.py`), and appended to the `forecast_list`.

The same is done for daily forecast.

Lastly, the index route sets the body class for the current conditions, resets the timezone, and renders the output using the `render_template` method from Flask.

<br>

### `utils.py` - Utilities & reusable code
The first module within `utils.py` is `DictObj`. This was sourced from [here](https://joelmccune.com/python-dictionary-as-object/). It allows dicts to be used as objects, making things easier to read and more succinct.

### `get_icon`
```python
get_icon(name: str, is_night: bool, chance_of_rain: float, chance_of_snow: float)
```

This returns an icon for the weather condition, time, and (if applicable) the portion of the icon that includes the chance of rain/snow.

The weather API has specific phrases, which are checked by this method.
For each match, the SVG file has its contents read, processed, and returned as valid HTML via Flask's `Markup` function.

### `get_day`
```python
get_day(date: str) -> str
```
Returns the day of the week (in word form) from a supplied input (as `str`).
It uses the built-in `datetime` library to process inputs and create outputs.

### `is_before_now`
```python
is_before_now(time: str) -> bool
```
Returns a boolean indicating whether or not a time is before the current system time.
It uses the built-in `datetime` library to process inputs and create outputs.

### `is_now`
```python
is_now(time: str) -> bool
```
Returns a boolean indicating whether or not a time is right now, based on the current system time.
It uses the built-in `datetime` library to process inputs and create outputs.

### `is_clear`
```python
is_clear(condition: str) -> bool
```
Returns a boolean indicating whether or not the current condition is sunny or not sunny (clear or not clear).
It uses the built-in `datetime` library to process inputs and create outputs.

### `is_night`
```python
is_night(input_current: str, input_today_dawn: str, input_today_dusk: str, input_tomorrow_dawn: str, input_tomorrow_dusk) -> bool
```
Returns a boolean indicating whether or not a time is night time.
It uses the built-in `datetime` library to process inputs and create outputs.

### `format_hour_forecast_obj`
```python
format_hour_forecast_obj(hour: object, today_sunrise: str, today_sunset: str, tomorrow_sunrise: str, tomorrow_sunset: str) -> Dict
```
Returns a `Dict` containing required elements for rendering the UI. Includes `time`, `icon`, and `detail`, which jinja uses when rendering.

### `tz_diff`
```python
tz_diff(home: str, away: str on=None)
```
Calculates the hourly difference between two timezones using the `pendulum` library (v.1.2.5). It was used when solving the Timezone problem, but is not currently used (may be useful in the future).

Sourced from [here](https://stackoverflow.com/questions/46736529/how-to-compute-the-time-difference-between-two-time-zones-in-python).

<br>

## Design Choices

The design for this application was based entirely on Apple's iOS Weather app, available on iOS. Using screenshots and MacOS's Digital Color Meter tool, I was able to get the exact colors used by Apple. Using my knowledge of CSS (and Google's), I was able to piece together a UI that closely resembles the app.

My goal when writing CSS is to write as little as possible, not to copy-paste any old google result into the project. I primarily used `flexbox` to align items and space items on screen, but in the 3-day (titled ten-day in the code) forecast, I used the `grid` feature in CSS to ensure items are properly spaced.

I used [this tool to build gradients](https://cssgradient.io/), [this tool to build shadows](https://shadows.brumm.af/).


## Contact

If you have any questions, comments, or concerns, feel free to [email me](mailto:mail@jacklabbe.com).

## Notice
This software is intended for demonstration purposes only and in no way is intended to provide highly accurate weather information. By use or modification of this software, you agree Jack Labbe is NOT responsible for any damages. Refer to the LICENSE for more information.
