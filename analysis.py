def count_skills(data):
    skill_counts = {}
    for job in data:
        for skill in job ['Skills']:
            if skill in skill_counts:
                skill_counts[skill] += 1
            else:
                skill_counts[skill] = 1
    return(skill_counts)

from scraper import extract, transform

jobs = extract()
data = transform(jobs)

counts = count_skills(data)
print(counts)