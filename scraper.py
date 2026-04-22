import requests
import pandas as pd

def extract():
    url = "https://remoteok.com/api"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    jobs = r.json()
    return jobs

def transform(jobs):
    jobs = jobs[1:]
    results = []
    for job in jobs:
        max_sal = job.get('salary_max', 0)
        min_sal = job.get('salary_min', 0)
        results.append({
            'Title' : job.get('position', 'N/A'),
            'Company' : job.get('company', 'N/A'),
            'Minimum Salary' : 'N/A' if min_sal == 0 else min_sal,
            'Maximum Salary' : 'N/A' if max_sal == 0 else max_sal,
            'Skills' : job.get('tags', 'N/A'),
            'Responsibilities' : job.get('description', 'N/A'),
            'Date' : job.get('date', 'N/A'),
            'URL' : job.get('url', 'N/A'),
            'Location' : job.get('location', 'N/A'),
        })
    return results

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} jobs to {filename}")

jobs = extract()
data = transform(jobs)
save_to_csv(data, 'jobs.csv')