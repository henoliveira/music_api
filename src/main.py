from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


api = FastAPI()

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
async def get_songs_list() -> List[str]:
    return get_songs_names_list(get_files_names_list())


@api.get("/song/{song_name}")
async def get_song(song_name: str) -> FileResponse:
    for file_name in get_files_names_list():
        song = get_song_from_file(file_name)
        if song.tag.title == song_name:
            return FileResponse(path=song.path, media_type="audio/mp3")
    raise HTTPException(status_code=404, detail="Song not found")


@api.post("/song")
async def upload_song(file: UploadFile):
    save_song_file(file)
    return file


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
