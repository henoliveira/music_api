from os import getcwd

from fastapi import FastAPI
from fastapi.responses import FileResponse

api = FastAPI()

CUR_DIR = getcwd()
SONGS_DIR = f"{CUR_DIR}/src/songs"


@api.get("/{file_name}")
def get_song(file_name: str):
    path = f"{SONGS_DIR}/{file_name}.mp3"
    return FileResponse(path=path, media_type="audio/mp3")
