"""Module for exploring data suplied by SMN enpoint

"ides"	int	id estado
"idmun"	int	id municipio
"nes"	string	nombre estado
"nmun"	string	nombre municipio
"dloc"	string	día local, inicia cuatro horas antes (YYYmmddhhmm)
"ndia"	int	número de día
"tmax"	int	Temperatura máxima (°C)
"tmin"	int	Temperatura mímima (°C)
"desciel"	string	Descripción del cielo
"probprec"	int	Probabilidad de precipitación (%)
"prec"	int	Precipitación (litros/m2)
"velvien"	int	Velocidad del viento (km/h)
"dirvienc"	int	Dirección del viento (Cardinal)
"dirvieng"	int	Dirección del viento (Grados)
"cc"	int	Cobertura de nubes (%)
"lat"	int	Latitud
"lon"	int	Longitud
"dh"	int	Diferencia respecto a hora UTC
"dsem"	int	Día de la semana
"temp"	int	Temperatura superficie (°C)
"hr"	int	Humedad relativa
"dpt"	int	Temperatura punto de rocío

Index(['desciel', 'dh', 'dirvienc', 'dirvieng', 'dpt', 'dsem', 'hloc', 'hr',
       'ides', 'idmun', 'lat', 'lon', 'nes', 'nhor', 'nmun', 'prec',
       'probprec', 'raf', 'temp', 'velvien'],
      dtype='object')

"""
import pandas as pd
from pathlib import Path
import gzip
import json

FILE_NAME = "DailyForecast_MX.gz"
# DATA_PATH = Path(__file__).resolve().parents[2].joinpath(FILE_NAME)
DATA_PATH = Path(__file__).resolve().parents[2].joinpath("test/data")

for item in DATA_PATH.iterdir():
    print(item)
file_path = DATA_PATH.joinpath(FILE_NAME)

with open(file_path, "rb") as f:
    content = f.read()
    data = gzip.decompress(content)
    data_str = data.decode("utf-8")
    json_data = json.loads(data_str)

df = pd.DataFrame(json_data)
# print(df.info())
# print(df.head())
# print(df["nes"].unique())
print(df.columns)
nmun = "Apodaca"
nes = "Nuevo León"
# filter = (df["nes"] == "Nuevo León") & (df["nmun"] == nmun)
# sel_columns = ["hr", "dsem", "hloc", "nhor", "lat",
#                "lon", "velvien", "temp", "probprec"]
# print(df[filter][sel_columns])
# print(df[filter].columns)
# print(df[filter].loc[["lat", "lon", "tmax", "tmin", "velvien", "temp"]])

# daily forecast
daily_filter = (df["nes"] == "Nuevo León") & (df["nmun"] == nmun)
df_daily = df[daily_filter]
sel_columns = ["nes", "nmun", "cc", "velvien",
               "dirvienc", "ndia", "dloc""", "tmax", "tmin"]
print(df_daily[sel_columns])
