import pandas as pd
from datetime import datetime

def calculate_score(weather_data_pd_serie):
    score = 0

    # Température
    temp = weather_data_pd_serie["temperature(°C)"]
    if 20 <= temp <= 28:
        score += 2.5
    elif 18 <= temp < 20 or 28 < temp <= 30:
        score += 1.25

    # Humidité
    humidity = weather_data_pd_serie["humidity(%)"]
    if humidity < 70:
        score += 1.5
    elif humidity < 80:
        score += 0.75

    # Vent
    wind = weather_data_pd_serie["wind(m/s)"]
    if wind < 3:
        score += 1
    elif wind < 5:
        score += 0.5

    # Pluie
    rain = weather_data_pd_serie["rain(mm)"]
    if rain == 0:
        score += 2
    elif rain < 1:
        score += 1
    elif rain < 3:
        score += 0.5

    # Nuages
    cloud = weather_data_pd_serie["cloud(%)"]
    if cloud < 50:
        score += 1
    elif cloud < 75:
        score += 0.5

    # Neige
    snow = weather_data_pd_serie["snowfall(mm)"]
    if snow == 0:
        score += 0.5

    # Durée du jour
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

# # Chargement du fichier
# df = pd.read_csv("data/processed/your_file.csv")

# # Calcul du score
# df["score"] = df.apply(calculate_score, axis=1)

# # Sauvegarde
# df.to_csv("data/processed/your_file_with_score.csv", index=False)
