import os
import pandas as pd
from io import StringIO


def add_city_id_and_city_name(file_path, corresponding_city):
    history_data_processed_path = "data/history_processed/global_history_weather.csv"
    if os.path.exists(history_data_processed_path):
        raise OSError(
            f"ERROR: the file in '{history_data_processed_path}' already exists"
        )

    with open(file_path, "r") as f:
        lines = f.readlines()

    split_index = next(
        i for i in range(1, len(lines)) if lines[i].startswith("location_id")
    )

    cities_weather_csv = "".join(lines[split_index:])
    global_history_df = pd.read_csv(StringIO(cities_weather_csv))

    global_history_df_with_city_id = global_history_df.merge(
        corresponding_city, on="location_id", how="left"
    )

    global_history_df_with_city_id.drop(columns=["location_id"], inplace=True)
    return global_history_df_with_city_id


# paris_barcelone_tokyo = pd.DataFrame(
#     {
#         "location_id": [0, 1, 2],
#         "city_id": [2988507, 3128760, 1850144],
#         "city": ["paris", "barcelone", "tokyo"],
#     }
# )
# add_city_id_and_city_name(
#     "data/history_raw/2020-05-01 to 2025-06-19/weather_montréal_marrakech.csv",
#     paris_barcelone_tokyo
# )


# montreal_marrakesh = pd.DataFrame(
#     {
#         "location_id": [0, 1],
#         "city_id": [6077243, 2542997],
#         "city": ["montréal", "marrakesh"],
#     }
# )
# add_city_id_and_city_name(
#     "data/history_raw/2020-05-01 to 2025-06-19/weather_montréal_marrakech.csv",
#     montreal_marrakesh
# )
