"""Module to handle weather request Apis"""

import asyncio
import httpx

response = requests.get(
    'https://api.stormglass.io/v2/weather/point',
    params={
        'lat': 58.7984,
        'lng': 17.8081,
        'params': 'windSpeed',
    },
    headers={
        'Authorization': 'example-api-key'
    }
)

# storm glass weather point request
url = "https://api.stormglass.io/v2/weather/point"
# Do something with response data.
json_data = response.json()
