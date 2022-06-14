from os import getcwd

from storage3 import create_client

url = "https://gwomsvlapasfvqkxsuyx.supabase.co/storage/v1"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3b21zdmxhcGFzZnZxa3hzdXl4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1NTE1MzM0NSwiZXhwIjoxOTcwNzI5MzQ1fQ.LEd0KZ2M-mbGpjbc_RR4mBdZPgTiVYM7W_qsscTq20Y"
headers = {"apiKey": key, "Authorization": f"Bearer {key}"}


if __name__ == "__main__":
    cur_dir = getcwd()
    storage = create_client(url, headers, is_async=False)
    # x = storage.list_buckets()
    # y = storage
    res = storage.from_("songs").upload("Love.mp3", cur_dir + "/Love.mp3")
    print(res)
