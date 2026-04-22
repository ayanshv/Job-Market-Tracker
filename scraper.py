import requests

def extract():
    url = "https://remoteok.com/api"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    jobs = r.json()
    return jobs

jobs = extract()
print(f"Total jobs found: {len(jobs)}")