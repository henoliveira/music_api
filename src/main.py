import eyed3
import uvicorn

from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client as create_supabase
from storage3 import create_client as create_bucket

# Env
sb_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnbWpkZ25ieXh4dWptdWZpZWljIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUyNDUyMTEsImV4cCI6MTk3MDgyMTIxMX0.buDTTbi9zcsYrCIhKHv3_DcF7hO3AwCwqhDsfp66ozQ"
sb_url = "https://rgmjdgnbyxxujmufieic.supabase.co"
sb_storage_url = f"{sb_url}/storage/v1"
sb_storage_headers = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}

# Config
api = FastAPI()
sb = create_supabase(sb_url, sb_key)
bucket = create_bucket(
    sb_storage_url, sb_storage_headers, is_async=False
).from_("songs")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@api.get("/songs")
def get_songs() -> Dict[str, Any]:
    res = dict(sb.table("Songs").select("*").execute())
    return res["data"]


@api.get("/song/{song_name}")
def get_song(song_name: str) -> Dict[str, Any]:
    res = dict(sb.table("Songs").select("*").eq("title", song_name).execute())
    return res["data"][0]


@api.get("/mp3_by_song_name/{song_name}")
def get_mp3_by_song_name(song_name: str) -> str:
    res = dict(sb.table("Songs").select("*").eq("title", song_name).execute())
    path = res["data"][0]["path"]
    return bucket.get_public_url(path)


@api.get("/artists")
def get_artists() -> List[str]:
    res = dict(sb.table("Songs").select("artist").execute())
    return list(dict.fromkeys(map(lambda item: item["artist"], res["data"])))


@api.get("/songs_by_artist/{artist_name}")
def get_songs_by_artist(artist_name: str) -> Dict[str, Any]:
    res = dict(sb.table("Songs").select("*").eq("artist", artist_name).execute())
    return res["data"]


@api.get("/albums")
def get_albums() -> List[str]:
    res = dict(sb.table("Songs").select("album").execute())
    return list(dict.fromkeys(map(lambda item: item["album"], res["data"])))


@api.get("/songs_by_album/{album_name}")
def get_songs_by_album(album_name: str) -> Dict[str, Any]:
    res = dict(sb.table("Songs").select("*").eq("album", album_name).execute())
    return res["data"]


@api.patch("/song")
def update_song(
    song_name: str, new_name: str = None, new_artist: str = None, new_album: str = None
):
    res = dict(sb.table("Songs").select("*").eq("title", song_name).execute())
    song_data = res["data"][0]
    data_to_update = {
        "path": f"{new_name}.mp3" if new_name else song_data["path"],
        "title": new_name or song_data["title"],
        "artist": new_artist or song_data["artist"],
        "album": new_album or song_data["album"],
    }
    if new_name:
        bucket.move(song_data["path"], f"{new_name}.mp3")
    res = dict(
        sb.table("Songs").update(data_to_update).eq("title", song_name).execute()
    )
    return res["data"][0]


@api.patch("/artist")
def update_artist(artist_name: str, new_artist_name: str):
    res = dict(
        sb.table("Songs")
        .update({"artist": new_artist_name})
        .eq("artist", artist_name)
        .execute()
    )
    return res["data"][0]


@api.patch("/album")
def update_album(album_name: str, new_album_name: str):
    res = dict(
        sb.table("Songs")
        .update({"album": new_album_name})
        .eq("album", album_name)
        .execute()
    )
    return res["data"][0]


@api.post("/song")
def upload_song(path: str):
    mp3 = eyed3.load(path)
    song: dict = {
        "path": f"{mp3.tag.title}.mp3",
        "title": mp3.tag.title,
        "artist": mp3.tag.artist,
        "album": mp3.tag.album,
    }
    try:
        bucket.upload(song["path"], path)
    except Exception:
        raise HTTPException(404, f"Failed to upload {song['path']}")
    try:
        res = dict(sb.table("Songs").insert(song).execute())
        return res["data"][0]
    except Exception:
        raise HTTPException(201, f"Uploaded {song['path']} in database")


@api.delete("/song/{song_name}")
def delete_song(song_name: str):
    bucket.remove([f"{song_name}.mp3"])
    res = dict(sb.table("Songs").delete().eq("title", song_name).execute())
    return res["data"][0]


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
