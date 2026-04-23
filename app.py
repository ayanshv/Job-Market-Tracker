import streamlit as st
import pandas as pd
from scraper import extract, transform, filter_by_skill
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