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

if json_data:
    nmun = "Apodaca"
    nes = "Nuevo León"
    dias_es = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo",
    }
    df = pd.DataFrame(json_data)
    for col in df.columns:
        print(col)
    df["date"] = pd.to_datetime(df["dloc"], format="%Y%m%dT%H")
    df["dow"] = df["date"].dt.weekday.map(dias_es)
    # df["dow"] = df["date"].dt.day_name(locale="es_ES")
    df["week"] = df["date"].dt.isocalendar().week
    daily_filter = (df["nes"] == nes) & (df["nmun"] == nmun)
    df_daily = df[daily_filter]
    sel_columns = ["cc", "velvien", "dirvienc", "probprec", "desciel",
                   "date", "dow", "tmax", "tmin"]
    weather_report = ""
    for row in df_daily[sel_columns].itertuples():
        header = f"{row.date} - {row.dow.capitalize()}".center(15, "*")
        weather_report += header + "\n"
        weather_report += f"\tCobertura de nubes: {row.cc} %\n"
        weather_report += f"\tCielo: {row.desciel}\n"
        weather_report += f"\tVelocidad de viento: {row.velvien}km/h\n"
        weather_report += f"\tDireccion de viento: {row.dirvienc}\n"
        weather_report += f"\tProb lluvia: {row.probprec} %\n"
        weather_report += f"\tProb lluvia: {row.probprec}\n"
        weather_report += f"\tTemperatura max: {row.tmax} °C\n"
        weather_report += f"\tTemperatura min: {row.tmin}°C\n"

    print(weather_report)
