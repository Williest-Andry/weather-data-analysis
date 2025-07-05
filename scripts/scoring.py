import pandas as pd
from datetime import datetime

def calculate_score(weather_data_pd_serie):
    score = 0

    # Temperature score
    temp = weather_data_pd_serie["temperature(°C)"]
    if 20 <= temp <= 28:
        score += 2.5
    elif 18 <= temp < 20 or 28 < temp <= 30:
        score += 1.25

    # Humidity score
    humidity = weather_data_pd_serie["humidity(%)"]
    if humidity < 70:
        score += 1.5
    elif humidity < 80:
        score += 0.75

    # Wind score
    wind = weather_data_pd_serie["wind(m/s)"]
    if wind < 3:
        score += 1
    elif wind < 5:
        score += 0.5

    # Rain score
    rain = weather_data_pd_serie["rain(mm)"]
    if rain == 0:
        score += 2
    elif rain < 1:
        score += 1
    elif rain < 3:
        score += 0.5

    # Cloud score
    cloud = weather_data_pd_serie["cloud(%)"]
    if cloud < 50:
        score += 1
    elif cloud < 75:
        score += 0.5

    # Snow score
    snow = weather_data_pd_serie["snowfall(mm)"]
    if snow == 0:
        score += 0.5

    # Day duration score 
    sunrise = datetime.strptime(
        str(weather_data_pd_serie["sunrise_local_hour"]), "%H:%M:%S"
    )
    sunset = datetime.strptime(
        str(weather_data_pd_serie["sunset_local_hour"]), "%H:%M:%S"
    )
    duration = (sunset.hour + sunset.minute / 60) - (sunrise.hour + sunrise.minute / 60)
    if duration >= 10:
        score += 1.5
    elif duration >= 8:
        score += 0.75

    return round(score, 2)
