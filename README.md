# Apple Weather App Clone

This is a clone of the Apple Weather app that comes preinstalled on most iOS devices.

## Features
- Get the weather for your current location (based on IP address)
- Get the weather for a specified location
- Working clock in the upper left-hand corner (just like on iPhones)

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

## Contact

If you have any questions, comments, or concerns, feel free to [email me](mailto:mail@jacklabbe.com).

## Notice
This software is intended for demonstration purposes only and in no way is intended to provide highly accurate weather information. By use or modification of this software, you agree Jack Labbe is NOT responsible for any damages. Refer to the LICENSE for more information.