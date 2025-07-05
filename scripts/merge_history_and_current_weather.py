import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.scoring import calculate_score

def merge_history_and_current_weather():
    history_data_dir = "data/history_processed/global_history_weather.csv"
    global_data_processed_dir = "data/global_processed/global_weather.csv"

    # Read history and global weather CSV file
    history_global_df = pd.read_csv(history_data_dir)
    global_processed_df = pd.read_csv(global_data_processed_dir)

    # Add score in the history rows
    history_global_df["daily_score(/10)"] = history_global_df.apply(
        lambda row: calculate_score(row),
        axis=1
    )

    # Concat history and global weather
    updated_global_processed_df = pd.concat(
        [history_global_df, global_processed_df], ignore_index=True
    )
    # Drop duplicated rows
    updated_global_processed_df = updated_global_processed_df.drop_duplicates(
        subset=["city_id", "extract_date"], keep="last"
    )

    # Rename all columns
    updated_global_processed_df.rename(
        columns={
            "city": "city_name",
            "temperature": "temperature(°C)",
            "sunrise": "sunrise_local_hour",
            "sunset": "sunset_local_hour",
            "humitidy":"humidity(%)",
            "wind": "wind(m/s)",
            "rain": "rain(mm)",
            "cloud": "cloud(%)",
            "snowfall": "snowfall(mm)",
        },
        inplace=True,
    )
    
    # Save the merged dataframe
    updated_global_processed_df.to_csv(global_data_processed_dir, index=False)


# merge_history_and_current_weather()
