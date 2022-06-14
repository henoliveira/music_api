_sb_url = "https://rgmjdgnbyxxujmufieic.supabase.co"
sb_storage_url = f"{_sb_url}/storage/v1"
sb_api_url = f"{_sb_url}/rest/v1"

_sb_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnbWpkZ25ieXh4dWptdWZpZWljIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTUyNDUyMTEsImV4cCI6MTk3MDgyMTIxMX0.buDTTbi9zcsYrCIhKHv3_DcF7hO3AwCwqhDsfp66ozQ"
sb_storage_headers = {"apikey": _sb_key, "Authorization": f"Bearer {_sb_key}"}
sb_api_headers = f"apikey: {_sb_key}, Authorization: Bearer {_sb_key}"
