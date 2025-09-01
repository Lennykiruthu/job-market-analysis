import os
import sqlite3
import pandas as pd
import ast
from collections import Counter
import plotly.express as px
import streamlit as st

# Source credientials from streamlit secrets
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

# Create data directory is missing then download sqlite database from kaggle
@st.cache_resource
def get_connection():
    os.makedirs("data", exist_ok=True)

    # Download if directory is empty
    if not os.listdir("data"):
        st.warning("No DB file found. Downloading from Kaggle...")
    os.system("kaggle datasets download -d lennykiruthu/linkedin-jobs-sqlite --unzip -p ./data")

    # Find the first .db file
    db_files = [f for f in os.listdir("data") if f.endswith(".db")]
    if not db_files:
        st.error("No .db file found in ./data after download!")
        return None

    db_path = os.path.join("data", db_files[0])

    return sqlite3.connect(db_path, check_same_thread=False)


# Initiate sqlite connection to database
conn = get_connection()
cur = conn.cursor()

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
selected_job_df = positions_df.query(f"cluster_name == '{selected_job}'")

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