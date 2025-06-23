import pandas as pd
import os
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.convert_date import to_local_hour
from scripts.convert_date import timezone_to_hour


def merge_weather(date):
    global_weather_dir = f"data/global_processed/global_weather.csv"
    os.makedirs(os.path.dirname(global_weather_dir), exist_ok=True)

    if os.path.exists(global_weather_dir):
        global_df = pd.read_csv(global_weather_dir)
    else:
        global_df = pd.DataFrame()
    global_df.rename(columns={"timezone": "timezone_hour"}, inplace=True)

    new_data = []
    daily_raw_dir = f"data/daily_raw/{date}"
    for csv_file in os.listdir(daily_raw_dir):
        if csv_file.startswith("weather_") and csv_file.endswith(".csv"):
            file_df = pd.read_csv(f"{daily_raw_dir}/{csv_file}")

            city_timezone = file_df.at[0, "timezone"]
            sunrise_timestamp = file_df.at[0, "sunrise"]
            sunset_timestamp = file_df.at[0, "sunset"]
            file_df.at[0, "sunrise"] = to_local_hour(sunrise_timestamp, city_timezone)
            file_df.at[0, "sunset"] = to_local_hour(sunset_timestamp, city_timezone)

            file_df.rename(columns={"timezone": "timezone_hour"}, inplace=True)
            file_df.at[0, "timezone_hour"] = timezone_to_hour(city_timezone)

            new_data.append(file_df)

    if not new_data:
        raise ValueError(f"NEW VALUES NOT FOUND FOR THE DATE: {date}")

    updated_df = pd.concat([global_df] + new_data, ignore_index=True)
    updated_df = updated_df.drop_duplicates(
        subset=["city_id", "extract_date"], keep="last"
    )

    updated_df.to_csv(global_weather_dir, index=False)
