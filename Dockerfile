FROM tiangolo/meinheld-gunicorn:python3.9
LABEL maintainer "Jack Labbe <jack@jacklabbe.com>"

ENV WEATHER_API_KEY="NOKEY"
ENV MODULE_NAME="app"
ENV APP_MODULE="app:app"
ENV PORT=8000
ENV HOST=0.0.0.0

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

EXPOSE 8000