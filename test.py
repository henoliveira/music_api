from os import getcwd
from storage3 import create_client
import env


if __name__ == "__main__":
    cur_dir = getcwd()
    storage = create_client(env.sb_storage_url, env.sb_headers, is_async=False)
    res = storage.list_buckets()
    print(res)
