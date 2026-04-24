import matplotlib.pyplot as plt
from config import CHART_FILENAME, TOP_SKILLS_COUNT, CHART_WIDTH, CHART_HEIGHT

def count_skills(data):
    skill_counts = {}
    for job in data:
        for skill in job ['Skills']:
            if skill in skill_counts:
                skill_counts[skill] += 1
            else:
                skill_counts[skill] = 1
    return(skill_counts)

def generate_chart(skill_counts):
    sorted_skills = sorted(skill_counts.items(), key = lambda x: x[1], reverse = True)
    top_20 = sorted_skills [:TOP_SKILLS_COUNT]
    skills = [item[0] for item in top_20]
    counts = [item[1] for item in top_20]
    plt.figure(figsize=(CHART_WIDTH, CHART_HEIGHT))
    plt.bar(skills, counts)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_FILENAME)
    plt.show()
    print("Chart saved as skills_chart.png")


if __name__ == "__main__":
    from scraper import extract, transform
    jobs = extract()
    data = transform(jobs)
    counts = count_skills(data)
    generate_chart(counts)
    print(counts)