# Imports
import os
from matplotlib import artist
from get_spotify_charts import get_charts
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy.types as type
import re


# Changes working directory to file location
#os.chdir(os.path.dirname(__file__))

# Creates connection with the SQLite Database
engine = create_engine('sqlite:///data/database.db', echo=False)

# Loads data into Pandas' DataFrame

list_of_countries = [
"us", "gb", "ae","ar","at","au", "be","bg", "bo", "br", "ca", "ch", 
"cl", "co", "cr", "cy", "cz", "de", "dk","do","ec", "ee", "eg", "es", 
"fi", "fr", "gr", "gt", "hk", "hn", "hu", "id", "ie", "il", "in", "is",
"it", "jp", "kr", "lt", "lu", "lv", "ma", "mx", "my", "ni", "nl", "no",
"nz", "pa", "pe", "ph", "pl", "pt", "py", "ro", "ru", "sa", "se", "sg", 
"sk", "sv", "th", "tr", "tw", "ua", "uy", "vn", "za"]


charts_dfs = []
for country in list_of_countries:
    charts_dfs.append(get_charts(country=country))

df = pd.concat(charts_dfs, keys=list_of_countries)
df = df.reset_index(level=0).rename(columns={'level_0':'country'})
df["artist"] = df["artist"].apply(lambda artist: str(artist.strip().split(',')))
df["streams"] = df["streams"].apply(lambda stream: int(stream.replace(',', '')))
df = df.convert_dtypes()

df.to_sql("charts", con=engine, if_exists="append", dtype={
    "date": type.String(),
    "country": type.String(),
    "url": type.String(),
    "img": type.String(),
    "position": type.Integer(),
    "track": type.String(),
    "artist": type.String(),
    "streams": type.Integer()
})