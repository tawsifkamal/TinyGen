import requests

url = 'http://localhost:8000/test'
with requests.get(url, headers=None, stream=True) as r:
    print(r.status_code)
    for line in r.iter_lines(chunk_size=1024):
        print(line)

