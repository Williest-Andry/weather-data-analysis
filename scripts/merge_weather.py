import pandas as pd
import os
import datetime

def merge_weather(date):
    global_weather_dir = f"data/daily-processed/global_weather.csv"
    os.makedirs(os.path.dirname(global_weather_dir), exist_ok=True)

    if os.path.exists(global_weather_dir):
        global_df = pd.read_csv(global_weather_dir)
    else:
        global_df = pd.DataFrame()

    new_data = []
    daily_raw_dir = f"data/daily_raw/{date}"
    for csv_file in os.listdir(daily_raw_dir):
       if csv_file.startswith("weather_") and csv_file.endswith(".csv"):
           new_data.append(pd.read_csv(f"{daily_raw_dir}/{csv_file}"))

    if not new_data:
        raise ValueError(f"NEW VALUES NOT FOUND FOR THE DATE: {date}")

    updated_df = pd.concat([global_df] + new_data, ignore_index=True)

    updated_df.to_csv(global_weather_dir, index=False) 
