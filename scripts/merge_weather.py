import pandas as pd
import os
from datetime import datetime


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
            file_df.at[0, "sunrise"] = datetime.fromtimestamp(
                file_df.at[0, "sunrise"] + city_timezone
            ).strftime("%H:%M:%S")
            file_df.at[0, "sunset"] = datetime.fromtimestamp(
                file_df.at[0, "sunset"] + city_timezone
            ).strftime("%H:%M:%S")

            file_df.rename(columns={"timezone": "timezone_hour"}, inplace=True)
            city_timezone_hour = city_timezone / 3600
            file_df.at[0, "timezone_hour"] = city_timezone_hour

            new_data.append(file_df)

    if not new_data:
        raise ValueError(f"NEW VALUES NOT FOUND FOR THE DATE: {date}")

    updated_df = pd.concat([global_df] + new_data, ignore_index=True)
    updated_df = updated_df.drop_duplicates(
        subset=["city_id", "extract_date"], keep="last"
    )

    updated_df.to_csv(global_weather_dir, index=False)
