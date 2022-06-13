from os import getcwd, walk
from typing import List, Union

import eyed3
from fastapi import FastAPI
from fastapi.responses import FileResponse

api = FastAPI()

CUR_DIR = getcwd()
SONGS_DIR = f"{CUR_DIR}/public/songs/"


@api.get("/")
def get_songs_list() -> List[str]:
    filenames: Union[List[str], List] = next(walk(SONGS_DIR), (None, None, []))[2]
    return list(map(lambda file: eyed3.load(SONGS_DIR + file).tag.title, filenames))


@api.get("/{song}")
def get_song(song: str) -> FileResponse:
    path = f"{SONGS_DIR}{song}.mp3"
    return FileResponse(path=path, media_type="audio/mp3")
