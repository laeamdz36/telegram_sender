"""Module to request a phrase of the day to the web API"""

import asyncio
import json
import httpx
import ssl
from app.logger import logger

URL1 = "https://proverbia.net/frase-del-dia"

URL2 = "https://frasedeldia.azurewebsites.net/api/phrase"


# 1 request
# process
# return, only one function is called to this module to retrive the data

def get_url() -> str:
    """Returne the scoped url"""

    return URL2


def permisive_context_phrase() -> ssl.SSLContext:
    """Get a permisive context to query public data to Conagua"""

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context


async def requester() -> str | None:
    """Request to the web apis the content data"""

    url = get_url()
    ssl_context = permisive_context_phrase()
    async with httpx.AsyncClient(verify=ssl_context) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            logger.error(e)
            data = None
        except httpx.RequestError as e:
            response = None
            logger.error(e)
            data = None
    return data


def format_data(json_data) -> str:
    """Formate the json data extracted from response"""

    message = f"'{json_data['phrase']}'\n"
    message += f"Autor: {json_data['author']}"
    return message


async def main():
    """Run main execution"""

    task = asyncio.create_task(requester())

    data = await task
    format_data(data)


if __name__ == "__main__":

    # execute standalone functions
    # request info data from url
    asyncio.run(main())
