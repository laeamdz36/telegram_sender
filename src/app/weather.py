"""Module to handle weather request Apis"""

import asyncio
import json
import gzip
import httpx
import ssl
import pandas as pd
from app.logger import logger

# Definition of enpoinst for producion and for dev test
# Global Scheme
# production
GZ_URL_1 = "/smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
GZ_URL_3 = "/smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"
# DEV
SCHEME_TEST = "http://"
# DEV_SEVER = "localhost"
DEV_SEVER = "192.168.68.112"
DEV_PORT = "8040"
# PROD
PROD_SERVER = "smn.conagua.gob.mx"
SCHEME_PROD = "https://"
ENPOINT_PATH = "/tools/GUI/webservices/"
PROD_PAGE = "index.php"


def permisive_context_smn() -> ssl.SSLContext:
    """Get a permisive context to query public data to Conagua"""

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context


def get_url(env: str) -> str | None:
    """
    Get the url to request the file

    Args:
        env (str): Selection for Prod or Test

    Returns:
        The url string to perform the requests
    """
    url = None
    if env == "test":
        url = SCHEME_TEST + DEV_SEVER + ":" + DEV_PORT + ENPOINT_PATH
    elif env == "prod":
        url = SCHEME_PROD + PROD_SERVER + ENPOINT_PATH + PROD_PAGE
    return url


def storm_glass_cfg():
    """Configs for storm glass API requests"""

    url = "https://api.stormglass.io/v2/weather/point"


async def request_file():
    """Request file to the endpoint (Prod/Test)"""

    url = get_url(env="prod")
    ssl_context = permisive_context_smn()
    # Usage of async with for miles of requests is costly
    print(url)
    params = {"method": 1}
    json_data = None
    async with httpx.AsyncClient(verify=ssl_context) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            zip_data = response.content
        except httpx.RequestError as e:
            zip_data = None
            response = None
            print(f"Error on request {e}")
    if zip_data:
        try:
            data = gzip.decompress(zip_data)
            data_str = data.decode("utf-8")
            json_data = json.loads(data_str)
        except OSError as e:

            logger.info("Error on zip data reading %s", e)
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
        df["date"] = pd.to_datetime(df["dloc"], format="%Y%m%dT%H")
        df["dow"] = df["date"].dt.weekday.map(dias_es)
        # df["dow"] = df["date"].dt.day_name(locale="es_ES")
        df["week"] = df["date"].dt.isocalendar().week
        daily_filter = (df["nes"] == nes) & (df["nmun"] == nmun)
        df_daily = df[daily_filter]
        sel_columns = ["cc", "velvien",
                       "date", "dow", "tmax", "tmin"]
        text = df_daily[sel_columns].to_string(index=False)
        print(text)
    return text


async def main():
    """Main execution for local test"""

    task = asyncio.create_task(request_file())
    await task

if __name__ == "__main__":

    asyncio.run(main())
