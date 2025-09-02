# ----------------------------- Imports ----------------------------- #
import os
import sqlite3
import pandas as pd
import ast
from collections import Counter
import plotly.express as px
import streamlit as st

# ----------------------------- Accessing Kaggle Credentials ----------------------------- #
# Source credientials from streamlit secrets
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]

# ----------------------------- Creating Sqlite connections ----------------------------- #
# Create data directory is missing then download sqlite database from kaggle
@st.cache_resource
def get_connection():
    os.makedirs("data", exist_ok=True)

    # Download if directory is empty
    # if not os.listdir("data"):
    #     st.warning("No DB file found. Downloading from Kaggle...")
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

# Source relevant visualizations tables
positions_df            = pd.read_sql("SELECT * FROM positions;", conn)
companies_df            = pd.read_sql("SELECT * FROM companies", conn)
company_specialities_df = pd.read_sql("SELECT * FROM company_specialities", conn)
industries_df           = pd.read_sql("SELECT * FROM industries", conn)
job_industries_df       = pd.read_sql("SELECT * FROM job_industries", conn)

# ----------------------------- Creating Streamlit App (Start) ----------------------------- #
# Title
st.title("STEM Job Analysis")

# Sidebar content
st.sidebar.title("Sidebar Controls")

# Store unique jobs titles created via clustering
unique_job_titles = positions_df["cluster_name"].unique()

# Make a dropdown
selected_job = st.sidebar.selectbox(
    "Select a job title:",
    sorted(unique_job_titles)
)

st.write("You selected:", selected_job)

# ----------------------------- Merging ----------------------------- #
# Merge job industries and industries to get the industry per job id then merge the new dataframe to positions 
# to link each job id to an industry.

merged_industries_df = pd.merge(job_industries_df, industries_df, on='industry_id', how='left')
merged_industries_df = pd.merge(positions_df, merged_industries_df, on='job_id', how='left')

# Merge positions and company to get the top hiring companies per cluster/feature engineered job title
merged_companies_df = pd.merge(positions_df, companies_df, on='company_id', how='left')

# Merge positions and company specialities to get the top hiring company's speciality per cluster/feature engineered job title
merged_companies_specialities_df = pd.merge(positions_df, company_specialities_df, on='company_id', how='left')

# ----------------------------- Visualization 1 (Top 30 skills per Job Title) ----------------------------- #
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

fig.update_layout(yaxis=dict(dtick=1), title={"x":0.5, "xanchor": "center", "yanchor": "top"},
    title_font=dict(size=24, family="Arial", color="black"))

st.plotly_chart(fig, use_container_width=True)

# ----------------------------- Visualization 2 (Top 30 Industries per Job Title) ----------------------------- #
selected_job_merged_industry_df = merged_industries_df.query(f"cluster_name == '{selected_job}'")

# Convert column to list so to use counter to count individual elements
industry_counts = Counter(selected_job_merged_industry_df['industry_name'].tolist())

# Select the top 30 most common industries, the result is a list of tuples in descending order.
top_30 = industry_counts.most_common(30)

# This unpacks the tuples into iterables of equal length
industries, industry_counts = zip(*top_30)

# Build a DataFrame from the top 30 industries
top_30_df = pd.DataFrame({
    "industry": industries,
    "count": industry_counts
})

# ✅ Plot bar chart
fig = px.bar(
    top_30_df.sort_values("count", ascending=True),
    x="count",
    y="industry",
    orientation="h",
    title=f"Top Industries for {selected_job} Roles",
    labels={"count": "Frequency (# of job postings)", "skill": "Skill"},
    height=600)

fig.update_layout(yaxis=dict(dtick=1))

st.plotly_chart(fig, use_container_width=True)

# ----------------------------- Visualization 3 (Top 5 Hiring Companies) ----------------------------- #
selected_job_merged_companies_df = merged_companies_df.query(f"cluster_name == '{selected_job}'")

# Convert column to list so to use counter to count individual elements
companies_counts = Counter(selected_job_merged_companies_df['company_name'].tolist())

# Select the top 5 most common companies in each cluster
top_5 = companies_counts.most_common(5)

companies, counts = zip(*top_5)

# Convert top 5 into a DataFrame
top_5_df = pd.DataFrame({
    "company": companies,
    "count": counts
})

# ✅ Plot treemap
fig = px.treemap(
    top_5_df,
    path=["company"],        # hierarchy — here just company names
    values="count",          # sizes
    color="count",           # color intensity by job postings
    color_continuous_scale="Viridis",  # similar to your matplotlib colormap
    title=f"Top 5 Companies Hiring {selected_job}"
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

st.plotly_chart(fig, use_container_width=True)

# ----------------------------- Visualization 4 (Top 5 Hiring Companies) ----------------------------- #
selected_job_merged_companies_specialities_df = merged_companies_specialities_df.query(f"cluster_name == '{selected_job}'")
selected_job_merged_companies_specialities_clean_df = selected_job_merged_companies_specialities_df.dropna(subset=['speciality'])

companies_specialities_counts = Counter(selected_job_merged_companies_specialities_clean_df['speciality'].tolist())

# Select the top 5 most common company specialities in each cluster
top_10 = companies_specialities_counts.most_common(10)

companies_specialities, speciality_counts = zip(*top_10)

# Convert top 5 into a DataFrame
top_10_df = pd.DataFrame({
    "company": companies_specialities,
    "count": speciality_counts
})

# ✅ Plot treemap
fig = px.treemap(
    top_10_df,
    path=["company"],        # hierarchy — here just company names
    values="count",          # sizes
    color="count",           # color intensity by job postings
    color_continuous_scale="Viridis",  # similar to your matplotlib colormap
    title=f"Top 10 Company Specialities in {selected_job}"
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

st.plotly_chart(fig, use_container_width=True)
