import pandas as pd
from io import StringIO


def charger_csv_avec_villes(path_fichier, correspondance_villes):
    # Lire tout le fichier CSV
    with open(path_fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # Trouver la ligne où commence la deuxième partie (celle avec les données météo)
    index_separation = next(
        i for i in range(1, len(lignes)) if lignes[i].startswith("location_id")
    )

    # Séparer en deux fichiers CSV virtuels
    csv_locations = "".join(lignes[:index_separation])
    csv_meteo = "".join(lignes[index_separation:])

    # Charger les deux en DataFrames
    df_meteo = pd.read_csv(StringIO(csv_meteo))

    # Fusionner avec les infos de ville
    df_final = df_meteo.merge(correspondance_villes, on="location_id", how="left")

    return df_final


correspondance = pd.DataFrame(
    {
        "location_id": [0, 1, 2],
        "city_id": [2988507, 3128760, 1850144],
        "city": ["paris", "barcelone", "tokyo"],
    }
)

# Charger le fichier et fusionner dynamiquement
df_resultat = charger_csv_avec_villes("data/history_raw/2020-05-01 to 2025-06-19/weather_paris_barcelone_tokyo.csv", correspondance)

print(df_resultat[df_resultat['location_id'] == 1])
