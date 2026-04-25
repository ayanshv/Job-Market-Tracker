import streamlit as st
import pandas as pd
from scraper import extract, transform, filter_by_skill, match_score
import matplotlib.pyplot as plt
from analysis import count_skills

st.set_page_config(
    page_title="Job Market Tracker",
    page_icon="favicon.png",
    layout="wide"
)

st.logo("favicon.png", size = "large")

st.title(f"Track the Job Market. Find your Edge.")
st.write(
    "A data-driven job tracking application that collects real-time listings from public APIs, processes and filters job data, and presents actionable insights to help users navigate the job market more effectively."
)

with st.spinner("Fetching jobs..."):
    jobs = extract()
    data = transform(jobs)

st.markdown(f"### **Total Jobs Found: {len(data)}**")

with st.sidebar:
    st.header("Search")
    skill = st.text_input("Enter desired position: ")

    st.divider()

    st.header("Job Match Score")

    user_skills_input = st.text_input("What are you proficient in? Examples: Python, SQL, 3D (comma separated)", "")

df = pd.DataFrame(data)



if skill:
    filtered = filter_by_skill(data, skill)
    if len(filtered) == 0:
        st.warning("No jobs found for that skill. Try another search.")
    else:
        df = pd.DataFrame(filtered)

st.dataframe(
    df[['Title', 'Company', 'Minimum Salary', 'Maximum Salary', 'Skills', 'Date', 'Location', 'URL']],
    column_config={
        "URL": st.column_config.LinkColumn("URL")
    }
)

if user_skills_input:
    st.subheader("Job Match Score")
    user_skills = [s.strip() for s in user_skills_input.split(',')]
    scored = []
    for job in data:
        score = match_score(job, user_skills)
        scored.append({**job, 'Match Score %': score})

    scored_df = pd.DataFrame(scored)
    scored_df = scored_df.sort_values('Match Score %', ascending=False)
    st.dataframe(scored_df[['Title', 'Company', 'Minimum Salary', 'Maximum Salary', 'Skills', 'Match Score %']].head(10))
st.subheader("Top 20 In-Demand Skills")
counts = count_skills(data)

sorted_skills = sorted(counts.items(), key = lambda x: x[1], reverse = True)
top_20 = sorted_skills[:20]
skills = [item[0] for item in top_20]
number = [item[1] for item in top_20]
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(skills, number)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

