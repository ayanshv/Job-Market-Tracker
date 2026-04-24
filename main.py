from scraper import extract, transform, save_to_csv
from analysis import count_skills, generate_chart

print("Fetching Jobs")

jobs = extract()
data = transform(jobs)

save_to_csv(data, 'jobs.csv')
counts = count_skills(data)
generate_chart(counts)

print(f"Done! Found {len(data)} Jobs")
print("Chart saved as skills_chart.png")
print("Data saved as jobs.csv")