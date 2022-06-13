from os import getcwd as _getcwd
from os import walk as _walk
from typing import List, Union

import eyed3 as _eyed3

_CUR_DIR = _getcwd()
_SONGS_DIR = f"{_CUR_DIR}/public/songs/"


def get_files_names_list(directory: str = _SONGS_DIR) -> Union[List[str], List]:
    return next(_walk(directory), (None, None, []))[2]


def get_songs_names_list(
    file_list: List[str], directory: str = _SONGS_DIR
) -> List[str]:
    return list(map(lambda file: _eyed3.load(directory + file).tag.title, file_list))


def get_song_from_file(file: str, directory: str = _SONGS_DIR):
    return _eyed3.load(directory + file)


def save_song_file(song_file, directory: str = _SONGS_DIR):
    with open(f"{directory}{song_file.filename}", "wb") as file:
        file.write(song_file.file.read())
