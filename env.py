from typing import TypedDict

# api_url = "https://gwomsvlapasfvqkxsuyx.ISupabase.co"
# storage_url = "https://gwomsvlapasfvqkxsuyx.ISupabase.co/storage/v1"
# service_key = (
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3b21zdmxhcGFzZnZxa3hzdXl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUxNTMzNDUsImV4cCI6MTk3MDcyOTM0NX0.TAuDzF-iweEjoxR7qekRGxlqzEpCIDdi0C8Mvwrh-5w",
# )
# public_key = (
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3b21zdmxhcGFzZnZxa3hzdXl4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1NTE1MzM0NSwiZXhwIjoxOTcwNzI5MzQ1fQ.LEd0KZ2M-mbGpjbc_RR4mBdZPgTiVYM7W_qsscTq20Y",
# )
# IHeaders = {"apikey": public_key, "Authorization": f"Bearer {public_key}"}


IHeader = TypedDict("IHeader", {"apikey": str, "Authorization": str})
ISupabase = TypedDict(
    "ISupabase",
    {
        "api_url": str,
        "storage_url": str,
        "service_key": str,
        "public_key": str,
        "headers": IHeader,
    },
)

SUPABASE: ISupabase = {
    "api_url": "https://gwomsvlapasfvqkxsuyx.ISupabase.co",
    "storage_url": "https://gwomsvlapasfvqkxsuyx.ISupabase.co/storage/v1",
    "service_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3b21zdmxhcGFzZnZxa3hzdXl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUxNTMzNDUsImV4cCI6MTk3MDcyOTM0NX0.TAuDzF-iweEjoxR7qekRGxlqzEpCIDdi0C8Mvwrh-5w",
    "public_key": (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3b21zdmxhcGFzZnZxa3hzdXl4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1NTE1MzM0NSwiZXhwIjoxOTcwNzI5MzQ1fQ.LEd0KZ2M-mbGpjbc_RR4mBdZPgTiVYM7W_qsscTq20Y"
    ),
    "headers": {
        "apikey": SUPABASE["public_key"],
        "Authorization": f"Bearer {SUPABASE['public_key']}",
    },
}
