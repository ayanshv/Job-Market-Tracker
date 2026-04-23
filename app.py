import streamlit as st
from scraper import extract, transform
from analysis import count_skills

st.title(f"Track the Job Market. Find your Edge.")
st.write(
    "A data-driven job tracking application that collects real-time listings from public APIs, processes and filters job data, and presents actionable insights to help users navigate the job market more effectively."
)

with st.spinner("Fetching jobs..."):
    jobs = count_skills
    data = extract()

st.metric("Total jobs found: ", len(data))