import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.add_id_and_name import add_city_id_and_city_name
from scripts.convert_date import format_iso_to_hour


def transform_history_data(csv_history_file, corresponding_city):
    # Create output directory if not exist
    os.makedirs("data/history_processed/", exist_ok=True)
    history_data_processed_path = "data/history_processed/global_history_weather.csv"
   
    # Load history data if exist
    if os.path.exists(history_data_processed_path):
        existing_history_df = pd.read_csv(history_data_processed_path)
    else:
        existing_history_df = pd.DataFrame()

    # Add city id and name
    global_history_df = add_city_id_and_city_name(csv_history_file, corresponding_city)

    # Convert from cm to mm
    global_history_df["snowfall_sum (cm)"] = (global_history_df["snowfall_sum (cm)"].astype(float) / 7).round(2)
    # Rename all columns
    global_history_df.rename(
        columns={
            "snowfall_sum (cm)": "snowfall_sum (mm)",
            "sunrise (iso8601)": "sunrise",
            "sunset (iso8601)": "sunset",
            "time": "extract_date",
            "temperature_2m_mean (°C)": "temperature",
            "relative_humidity_2m_mean (%)": "humidity",
            "rain_sum (mm)": "rain",
            "snowfall_sum (cm)": "snowfall",
            "cloud_cover_mean (%)": "cloud",
            "wind_speed_10m_mean (m/s)": "wind",
        },
        inplace=True,
    )

    # Transform to hour
    global_history_df["sunrise"] = global_history_df.apply(
        lambda row: (format_iso_to_hour(row["sunrise"])), axis=1
    )
    global_history_df["sunset"] = global_history_df.apply(
        lambda row: (format_iso_to_hour(row["sunset"])), axis=1
    )

    # Column order
    ordered_global_history_df = global_history_df[
        [
            "city_id",
            "city",
            "extract_date",
            "temperature",
            "sunrise",
            "sunset",
            "humidity",
            "wind",
            "rain",
            "cloud",
            "snowfall",
        ]
    ]

    # Concat and save
    final_global_history_df = pd.concat([existing_history_df] + [ordered_global_history_df], ignore_index=True)
    final_global_history_df = final_global_history_df.drop_duplicates(subset=['city_id', 'extract_date'], keep='last')

    final_global_history_df.to_csv(history_data_processed_path, index=False)

    return ordered_global_history_df


paris_barcelone_tokyo = pd.DataFrame(
    {
        "location_id": [0, 1, 2],
        "city_id": [2988507, 3128760, 1850144],
        "city": ["paris", "barcelone", "tokyo"],
    }
)

montreal_marrakesh = pd.DataFrame(
    {
        "location_id": [0, 1],
        "city_id": [6077243, 2542997],
        "city": ["montréal", "marrakesh"],
    }
)

transform_history_data(
    "data/history_raw/2020-05-01 to 2025-06-19/weather_montréal_marrakech.csv",
    montreal_marrakesh,
)
transform_history_data(
    "data/history_raw/2020-05-01 to 2025-06-19/weather_paris_barcelone_tokyo.csv",
    paris_barcelone_tokyo
)