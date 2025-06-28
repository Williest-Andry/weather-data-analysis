import os
import pandas as pd

def dataset_to_star_schema():
    global_weather_dir = "data/global_processed/global_weather.csv" 
    star_schema_dir = "data/star_schema/"

    os.makedirs(os.path.dirname(star_schema_dir), exist_ok=True)

    global_df = pd.read_csv(global_weather_dir)

    dimension_city_df = global_df[["city_id", "city_name"]]
    dimension_city_df = dimension_city_df.drop_duplicates(
        subset=["city_id"],
        keep="first"
    )
    dimension_city_df.to_csv(f"{star_schema_dir}/dim_city.csv", index=False)

    global_df.drop(columns=["city_name"], inplace=True)
    global_df.to_csv(f"{star_schema_dir}/fact_weather.csv", index=False)
