from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import yt_dlp


class DownloadRequest(BaseModel):
    url: str


logger = logging.getLogger("fastapi")
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_media(url: str):
    params = {
        "format": "best",
        "outtmpl": f"/download/%(title)s.%(ext)s",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(params) as ytd:
        ytd.download(url)



@app.post("/")
def download_request_handler(download_request: DownloadRequest,background_tasks: BackgroundTasks):
    logger.info('Heloooo')
    background_tasks.add_task(download_media, download_request.url)
    return download_request
