"""Module to handle weather request Apis"""

import asyncio
import httpx
import gzip
from app.logger import logger

# get data from the SMN


async def process_url1():
    """Get data from the url1 fro SMN (Servicio Meteorologico Nacional)"""

    # # api for data forecast by hour and by 48 hours
    GZ_URL_3 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"
    # request data from the endpoint
    logger.info("Requesting info from -> %s",  GZ_URL_3)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(GZ_URL_3)
            response.raise_for_status()
            zip_data = response.content
        except httpx.RequestError as e:
            logger.info("Erorr on request %s - %s", GZ_URL_3, e)

    # process in memory zip data
    try:
        uncompressed_data = gzip.decompress(zip_data)
        uncompressed_data_str = uncompressed_data.decode()

    except OSError as e:
        logger.info("Error on zip data reading %s", e)


# storm glass weather point request
url = "https://api.stormglass.io/v2/weather/point"
# Do something with response data.


async def main_weather():
    """Masin execution loop for local test"""

    # create task for url1
    task_url1 = asyncio.create_task(process_url1())
    await task_url1

# local test
if __name__ == "__main__":
    asyncio.run(main_weather())
