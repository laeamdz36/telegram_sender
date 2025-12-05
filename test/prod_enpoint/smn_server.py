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
