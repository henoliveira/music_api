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
bucket = create_bucket(sb_storage_url, sb_storage_headers, is_async=False).from_(
    "songs"
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@api.get("/song", tags=["Songs"])
def get_songs() -> Dict[str, Any]:
    res = dict(
        sb.table("Songs").select("*").execute(),
    )
    return res["data"]


@api.get("/artist", tags=["Artists"])
def get_artists() -> List[str]:
    res = dict(
        sb.table("Songs").select("artist").execute(),
    )
    return list(dict.fromkeys(map(lambda item: item["artist"], res["data"])))


@api.get("/album", tags=["Albums"])
def get_albums() -> List[str]:
    res = dict(
        sb.table("Songs").select("album").execute(),
    )
    return list(dict.fromkeys(map(lambda item: item["album"], res["data"])))


@api.patch("/song", tags=["Songs"])
def update_song(
    id: str, new_name: str = None, new_artist: str = None, new_album: str = None
):
    res = dict(
        sb.table("Songs").select("*").eq("id", id).execute(),
    )
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
        sb.table("Songs").update(data_to_update).eq("id", id).execute(),
    )
    return res["data"][0]


@api.patch("/song/{name}/like", tags=["Songs"])
def update_liked_status(name: str):
    res = dict(
        sb.table("Songs").select("*").eq("title", name).execute(),
    )
    res = dict(
        sb.table("Songs")
        .update({"liked": not res["data"][0]["liked"]})
        .eq("title", name)
        .execute()
    )
    return res["data"][0]


@api.patch("/artist", tags=["Artists"])
def update_artist(name: str, new_name: str):
    res = dict(
        sb.table("Songs").update({"artist": new_name}).eq("artist", name).execute()
    )
    return res["data"][0]


@api.patch("/album", tags=["Albums"])
def update_album(name: str, new_name: str):
    res = dict(
        sb.table("Songs").update({"album": new_name}).eq("album", name).execute()
    )
    return res["data"][0]


@api.post("/song", tags=["Songs"])
def upload_song(path: str):
    mp3 = eyed3.load(path)
    mp3_path = f"{mp3.tag.title}.mp3"
    res = ""

    try:
        res = bucket.upload(mp3_path, path)
    except Exception:
        raise HTTPException(404, f"Failed to upload {mp3_path}")

    public_url = str(res.url).replace("object/songs", "object/public/songs")

    song: dict = {
        "path": mp3_path,
        "title": mp3.tag.title,
        "artist": mp3.tag.artist,
        "album": mp3.tag.album,
        "duration": mp3.info.time_secs,
        "public_url": public_url,
    }

    try:
        res = dict(sb.table("Songs").insert(song).execute())
        return res["data"][0]
    except Exception:
        raise HTTPException(201, f"Uploaded {song['path']} in database")


@api.delete("/song", tags=["Songs"])
def delete_song(name: str):
    bucket.remove([f"{name}.mp3"])
    res = dict(
        sb.table("Songs").delete().eq("title", name).execute(),
    )
    return res["data"][0]


@api.post("/playlist", tags=["Playlists"])
def create_playlist(name: str):
    res = dict(
        sb.table("Playlists").insert({"name": name}).execute(),
    )
    return res["data"][0]


@api.get("/playlist", tags=["Playlists"])
def get_playlists():
    res = dict(
        sb.table("Playlists").select("*, songs:PlaylistSong(data:Songs(*))").execute()
    )
    return res["data"]


@api.delete("/playlist", tags=["Playlists"])
def delete_playlist(id: str):
    sb.table("PlaylistSong").delete().eq("playlist_id", id).execute()
    res = dict(
        sb.table("Playlists").delete().eq("id", id).execute(),
    )
    return res["data"][0]


@api.patch("/playlist", tags=["Playlists"])
def update_playlist_name(id: str, new_name: str):
    res = dict(
        sb.table("Playlists").update({"name": new_name}).eq("id", id).execute(),
    )
    return res["data"][0]


@api.patch("/playlist/{playlist_id}/add_song", tags=["Playlists"])
def add_song_to_playlist(playlist_id: str, song_id: str):
    res = dict(
        sb.table("PlaylistSong")
        .insert(
            {
                "playlist_id": playlist_id,
                "song_id": song_id,
            }
        )
        .execute()
    )
    return res["data"][0]


if __name__ == "__main__":
    uvicorn.run("__main__:api", host="0.0.0.0", port=8000, reload=True)
