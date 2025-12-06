"""Smulation of prod server for weather"""

from fastapi import FastAPI
from starlette.responses import FileResponse
from pathlib import Path
import os

app = FastAPI()

# definition of name of files
FILE_HOURLY = "HourlyForecast_MX.gz"
FILE_DAILY = "DailyForecast_MX.gz"

# Enpoints
# GZ_URL_1 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
# GZ_URL_3 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"
GZ_URL_1 = "/smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
GZ_URL_3 = "/smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"


def get_path(file_name: str) -> Path:
    """Get thje working path for the selected file (Hourly or Daily)"""

    file_name = file_name.capitalize() + "Forecast_MX.gz"
    path = Path(__file__).resolve().parents[1].joinpath(f"data/{file_name}")
    if path.exists():
        return path


def get_path_int(selection: int) -> Path:
    """Get the file path to serve by integer selection"""

    file_name = None
    if selection == 1:
        file_name = FILE_DAILY
    elif selection == 3:
        file_name = FILE_HOURLY
    if file_name:
        path = Path(__file__).resolve().parents[1].joinpath(
            f"data/{file_name}")
    if path.exists():
        return path


@app.get(GZ_URL_1)
async def serve_file_1():
    """Serve the file for the --host 0.0.0.0 --port 8040"""

    file_path = Path(__file__).resolve(
    ).parents[1].joinpath(f"data/{FILE_DAILY}")
    if not file_path.exists():
        return {"error": "File not found", "path": "file_path"}
    media_type = "application/x-gzip" if FILE_DAILY.endswith(
        ".gz") else "application/zip"

    return FileResponse(path=file_path, media_type=media_type, filename=os.path.basename(FILE_DAILY))


@app.get(GZ_URL_3)
async def serve_file_3():
    """Test endpoint for file enpoinr SMN method 3"""

    response = None
    path = get_path("hourly")
    if path:
        media_type = "application/x-gzip" if FILE_DAILY.endswith(
            ".gz") else "application/zip"
        response = FileResponse(
            path=path, media_type=media_type, filename=os.path.basename("hourly"))
    else:
        response = {"status": "not Found"}
    return response


# methode with query parameters
@app.get("/tools/GUI/webservices/")
async def serve_file(method: int):
    """Enpoint for test and emulate the prduction server"""

    response = None
    path = get_path_int(method)
    if path:
        media_type = "application/x-gzip"
        response = FileResponse(
            path=path, media_type=media_type, filename=os.path.basename(path.name))
    else:
        response = {"status": "not Found"}
    return response
