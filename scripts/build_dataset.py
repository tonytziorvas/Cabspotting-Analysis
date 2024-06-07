import os

import geopandas as gpd
import pandas as pd


def create_dataset(files):
    """The function reads multiple CSV files, processes the data
    creates a GeoDataFrame, and saves it to a CSV file.

    Parameters
    ----------
    files
        A list of file paths.

    Returns
    -------
        A GeoDataFrame `gdf` containing the dataset created from the input files.
        The dataset is then saved to a CSV file named "cabspotting_full.csv".

    """
    df_list = []

    for file in files:
        temp = pd.read_csv(
            file, sep=" ", names=["lat", "lon", "occupancy", "timestamp"]
        )
        temp["taxi_id"] = os.path.basename(files[0]).split(".")[0].split("_")[-1]
        df_list.append(temp)

    df = pd.concat(df_list, axis=0, ignore_index=True).reindex(
        columns=["taxi_id", "timestamp", "latitude", "longitude", "occupancy"]
    )

    gdf = gpd.GeoDataFrame(
        data=df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs=4326,
    ).rename(  # type: ignore
        {"geometry": "location"},
        axis=1,
    )

    print(f"The Dataset contains {gdf.shape[0]} rows and {gdf.shape[1]} columns")

    gdf.to_csv("../csv/cabspotting_full.csv", index=False)


if __name__ == "__main__":

    # Read the content of the data root directory
    files = [
        f"{'./alldata'}/{file}"
        for file in os.listdir("./alldata")
        if file.startswith("new_")
    ]

    create_dataset(files)
