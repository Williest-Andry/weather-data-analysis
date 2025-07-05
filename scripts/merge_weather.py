import pandas as pd
import os
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.convert_date import to_local_hour
from scripts.convert_date import timezone_to_hour
from scripts.scoring import calculate_score

def merge_weather(date):
    # Create output file if not exist
    global_weather_dir = f"data/global_processed/global_weather.csv"
    os.makedirs(os.path.dirname(global_weather_dir), exist_ok=True)

    # Load existing data if exist
    if os.path.exists(global_weather_dir):
        global_df = pd.read_csv(global_weather_dir)
    else:
        global_df = pd.DataFrame()

    # Read new daily file
    new_data = []
    daily_raw_dir = f"data/daily_raw/{date}"
    for csv_file in os.listdir(daily_raw_dir):
        if csv_file.startswith("weather_") and csv_file.endswith(".csv"):
            file_df = pd.read_csv(f"{daily_raw_dir}/{csv_file}")

            # Retrieve timezone, sunrise and sunset
            city_timezone = file_df.at[0, "timezone"]
            sunrise_timestamp = file_df.at[0, "sunrise"]
            sunset_timestamp = file_df.at[0, "sunset"]
            # Convert sunrise and sunset to local hour
            file_df.at[0, "sunrise"] = to_local_hour(sunrise_timestamp, city_timezone)
            file_df.at[0, "sunset"] = to_local_hour(sunset_timestamp, city_timezone)

            # Rename all columns
            file_df.rename(
                columns={
                    "timezone": "timezone_hour",
                    "snow": "snowfall",
                    "city": "city_name",
                    "temperature": "temperature(°C)",
                    "sunrise": "sunrise_local_hour",
                    "sunset": "sunset_local_hour",
                    "humidity": "humidity(%)",
                    "wind": "wind(m/s)",
                    "rain": "rain(mm)",
                    "cloud": "cloud(%)",
                    "snow": "snowfall(mm)",
                },
                inplace=True,
            )
            # Timezone from second to hour
            file_df.at[0, "timezone_hour"] = timezone_to_hour(city_timezone)

            # Drop 'description' column
            file_df.drop(columns=["description"], inplace=True)

            # Modify the extract_date format
            file_df.at[0, "extract_date"] = datetime.strptime(
                str(file_df.at[0, "extract_date"]), "%Y-%m-%d"
            ).date()

            # Define the column order
            file_df = file_df[
                [
                    "city_id",
                    "city_name",
                    "extract_date",
                    "temperature(°C)",
                    "sunrise_local_hour",
                    "sunset_local_hour",
                    "humidity(%)",
                    "wind(m/s)",
                    "rain(mm)",
                    "cloud(%)",
                    "snowfall(mm)",
                ]
            ]
            
            # Add score for each rows
            file_df["daily_score(/10)"] = file_df.apply(
                lambda row: calculate_score(row),
                axis=1
            )

            new_data.append(file_df)

    if not new_data:
        raise ValueError(f"NEW VALUES NOT FOUND FOR THE DATE: {date}")

    # Concat the dataframe and drop duplicated rows
    updated_df = pd.concat([global_df] + new_data, ignore_index=True)
    updated_df = updated_df.drop_duplicates(
        subset=["city_id", "extract_date"], keep="last"
    )

    # Save into CSV file 
    updated_df.to_csv(global_weather_dir, index=False)
