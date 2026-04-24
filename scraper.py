from datetime import datetime
import requests
import re
import html
import pandas as pd
from config import API_URL, USER_AGENT, CSV_FILENAME

def strip_html(text):
    if text == 'N/A':
        return 'N/A'
    text = re.sub('<.*?>', '', text)
    text = html.unescape(text)
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    text = re.sub(r'â\w*', '', text)
    text = re.sub(r'\*\*.*?\*\*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%B %d, %Y")
    except:
        return 'N/A'

def extract():
    url = API_URL
    headers = {'User-Agent': USER_AGENT}
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
            'Minimum Salary' : 'Please check the URL for salary information' if min_sal == 0 else min_sal,
            'Maximum Salary' : 'Please check the URL for salary information' if max_sal == 0 else max_sal,
            'Skills' : job.get('tags', 'N/A'),
            'Responsibilities': strip_html(job.get('description', 'N/A')),
            'Date': format_date(job.get('date', 'N/A')),
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

def match_score(job, user_skills):
    job_skills = job.get('Skills', [])
    if not job_skills or job_skills == 'N/A':
        return 0
    matches = sum(
        1 for skill in job_skills
        if any(skill.lower() == user_skill.lower()
               for user_skill in user_skills)
    )
    return int((matches/ len(job_skills)) * 100)


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

