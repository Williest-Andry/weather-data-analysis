import requests
import os
import pandas as pd
import logging
from datetime import datetime

def extract_city_weather(city, date, api_key):
    try:
        API_URL = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        data = response.json()

        actual_date = datetime.strptime(str(date), "%Y-%m-%d")
        weather_data = {
            "city_id": data["id"],
            "city": city,
            "extract_date": actual_date,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"],
            "timezone": data["timezone"],
            "snow": data.get("rain", {}).get("1h", 0),
            "rain": data.get("snow", {}).get("1h", 0),
            "cloud": data["clouds"]["all"],
        }

        raw_data_dir = f"data/daily_raw/{actual_date.date()}/"
        os.makedirs(os.path.dirname(raw_data_dir), exist_ok=True)

        pd.DataFrame([weather_data]).to_csv(
            f"{raw_data_dir}/weather_{city}.csv", index=False
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"API REQUEST ERROR: {e}")
    except Exception as e:
        logging.error(f"UNEXPECTED ERROR WHEN EXTRACT DATA: {e}")
