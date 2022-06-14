import uvicorn
import env

from typing import List
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from supabase import Client, create_client as create_supabase
from storage3 import create_client as create_bucket


api = FastAPI()
sb = create_supabase(env.sb_api_url, env.sb_headers)


origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/songs")
def get_songs_list() -> List[str]:
    pass


@api.get("/song/{song_name}")
def get_song(song_name: str) -> FileResponse:
    pass


@api.post("/song")
def upload_song(file: UploadFile):
    pass


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
