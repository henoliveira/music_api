from os import getcwd

from fastapi import FastAPI
from fastapi.responses import FileResponse

api = FastAPI()


@api.get("/{music_name}")
def get_video(music_name: str):
    path = f"{getcwd()}/{music_name}"
    return FileResponse(path=path, media_type="audio/mp3")
