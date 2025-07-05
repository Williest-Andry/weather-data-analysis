import os
import pandas as pd

def dataset_to_star_schema():
    global_weather_dir = "data/global_processed/global_weather.csv" 
    star_schema_dir = "data/star_schema/"

    # Create output file
    os.makedirs(os.path.dirname(star_schema_dir), exist_ok=True)

    # Read the existing global weather
    global_df = pd.read_csv(global_weather_dir)

    # Create the city dimension table 
    dimension_city_df = global_df[["city_id", "city_name"]]
    dimension_city_df = dimension_city_df.drop_duplicates(
        subset=["city_id"],
        keep="first"
    )
    # Save the dim city table
    dimension_city_df.to_csv(f"{star_schema_dir}/dim_city.csv", index=False)

    global_df.drop(columns=["city_name"], inplace=True)
    # Save the fact table 
    global_df.to_csv(f"{star_schema_dir}/fact_weather.csv", index=False)
