FROM python:latest

RUN pip install --upgrade pip
RUN pip install pyowm

COPY getweather.py /weather-py/
WORKDIR /weather-py/


CMD [ "python", "getweather.py" ]