import os
import pandas as pd
from io import StringIO


def add_city_id_and_city_name(file_path, corresponding_city):
    # Read the file 
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Go to the next line which contains location_id
    split_index = next(
        i for i in range(1, len(lines)) if lines[i].startswith("location_id")
    )

    # Transform to dataframe
    cities_weather_csv = "".join(lines[split_index:])
    global_history_df = pd.read_csv(StringIO(cities_weather_csv))

    # Make merge with criteria
    global_history_df_with_city_id = global_history_df.merge(
        corresponding_city, on="location_id", how="left"
    )

    # Drop location_id column
    global_history_df_with_city_id.drop(columns=["location_id"], inplace=True)

    return global_history_df_with_city_id
