import streamlit as st
import pandas as pd
from scraper import extract, transform, filter_by_skill
import matplotlib.pyplot as plt
from analysis import count_skills

st.title(f"Track the Job Market. Find your Edge.")
st.write(
    "A data-driven job tracking application that collects real-time listings from public APIs, processes and filters job data, and presents actionable insights to help users navigate the job market more effectively."
)

with st.spinner("Fetching jobs..."):
    jobs = extract()
    data = transform(jobs)

st.metric("Total jobs found: ", len(data))

df = pd.DataFrame(data)

skill = st.text_input("Enter desired position: ")

if skill:
    filtered = filter_by_skill(data, skill)
    df = pd.DataFrame(filtered)

st.dataframe(df)


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

