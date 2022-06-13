from os import getcwd, walk
from typing import List, Union

from fastapi import FastAPI
from fastapi.responses import FileResponse

api = FastAPI()

CUR_DIR = getcwd()
SONGS_DIR = f"{CUR_DIR}/public/songs"


@api.get("/")
def get_songs_names() -> Union[List[str], List]:
    return next(walk(SONGS_DIR), (None, None, []))[2]


@api.get("/{file_name}")
def get_song(file_name: str) -> FileResponse:
    path = f"{SONGS_DIR}/{file_name}.mp3"
    return FileResponse(path=path, media_type="audio/mp3")
