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

def filter_by_skill(data, skills):
    jobs = []
    for job in data:
        for tag in job['Skills']:
            if skills.lower() == tag.lower():
                jobs.append(job)
                break
    return jobs

if __name__ == "__main__":
    jobs = extract()
    data = transform(jobs)
    save_to_csv(data, 'jobs.csv')
    skill = input("Enter desired position: ")
    filtered = filter_by_skill(data, skill)
    if len(filtered) == 0:
        print("No jobs currently available for this position. Please try again later.")
    else:
        print(f"Found {len(filtered)} job(s) for '{skill}'")
        save_to_csv(filtered, f'{skill}_jobs.csv')