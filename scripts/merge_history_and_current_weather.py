import pandas as pd

def merge_history_and_current_weather():
    history_data_dir = "data/history_processed/global_history_weather.csv"
    global_data_processed_dir = "data/global_processed/global_weather.csv"

    history_global_df = pd.read_csv(history_data_dir)
    global_processed_df = pd.read_csv(global_data_processed_dir)

    updated_global_processed_df = pd.concat(
        [history_global_df, global_processed_df], ignore_index=True
    )
    updated_global_processed_df = updated_global_processed_df.drop_duplicates(
        subset=["city_id", "extract_date"], keep="last"
    )

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
    
    updated_global_processed_df.to_csv(global_data_processed_dir, index=False)


merge_history_and_current_weather()
