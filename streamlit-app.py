import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# Source credientials from streamlit secrets
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

# Create data directory is missing then download sqlite database from kaggle
def get_connection():
    db_path = "data/linkedin_jobs.db"

    if not os.path.exists(db_path):
        os.makedirs("data", exist_ok=True)

        # Download data via Kaggle
        os.system("kaggle datasets -d lennykiruthu/linkedin-jobs-sqlite --unzip -p ./data")

        return sqlite3.connect(db_path)

# Initiate sqlite connection to database
conn = get_connection()

# Source positions table
positions_df = pd.read_sql("SELECT * FROM positions;", conn)

# Store unique jobs titles created via clustering
unique_job_titles = positions_df["cluster_name"].unique()

# Make a dropdown
selected_job = st.selectbox(
    "Select a jo title:",
    sorted(unique_job_titles)
)

st.write("You selected:", selected_job)

# Select dataframe subset
selected_job_df = stem_positions_df.query(f"cluster_name == '{selected_job}'")

# Convert strings to actual Python lists
selected_job_df["cluster_skills"] = selected_job_df["cluster_skills"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# ✅ Count unique skills per row
skill_counts = Counter()

for skills in selected_job_df["cluster_skills"]:
    unique_skills = set(skills)  # remove duplicates in the same row
    skill_counts.update(unique_skills)

# ✅ Convert to DataFrame for easy plotting
skills_df = pd.DataFrame(skill_counts.items(), columns=["skill", "count"]).sort_values(by="count", ascending=False)

# ✅ Plot bar chart
fig = px.bar(
    skills_df.sort_values("count", ascending=True),
    x="count",
    y="skill",
    orientation="h",
    title=f"Top skills for {selected_job} Roles",
    labels={"count": "Frequency (# of job postings)", "skill": "Skill"},
    height=600)

fig.update_layout(yaxis=dict(dtick=1))

st.plotly_chart(fig, use_container_width=True)