## STEM Job Market Analysis
This repository contains a comprehensive analysis of STEM-related job postings, sourced from LinkedIn, and provides an interactive dashboard for exploring job clusters, top skills, hiring industries, and companies.
### Source
This dataset is derived from:  
Arsh Koneru. (2024). LinkedIn Job Postings (2023 - 2024) [Data set].  
Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9200871  

### License
This dataset is shared under the same license as the original:  
Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
The dataset contains multiple CSV files including:

- `companies.csv`
- `company_industries.csv`
- `company_specialities.csv`
- `employee_counts.csv`
- `benefits.csv`
- `job_industries.csv`
- `job_skills.csv`
- `salaries.csv`
- `industries.csv`
- `skills.csv`
- `postings.csv`
Additionally, I created an **engineered version of this dataset**, transformed into an SQLite database for structured querying, which is available here: [LinkedIn Jobs SQLite Database](https://www.kaggle.com/datasets/lennykiruthu/linkedin-jobs-sqlite)

## Project Workflow
### 1. Data Ingestion
- Explored relationships between the CSV files using unique identifiers (`job_id`, `company_id`, `industry_id`).
- Created an **SQLite database** to host the data for easier querying and reproducibility.  
- Published the SQLite database on Kaggle: [LinkedIn Jobs SQLite](https://www.kaggle.com/datasets/lennykiruthu/linkedin-jobs-sqlite?utm_source=chatgpt.com)

### 2. Feature Engineering
- Filtered job titles containing STEM-related keywords:
 ```python
stem_list = ['Data', 'Software', 'Engineer', 'Math', 'Account', 'Finance', 'Biology', 'Physics','Cloud', 'Full Stack', 'AI', 'ML', 'Machine Learning', 'Deep Learning', 'DevOps','Backend', 'Mechanical', 'Electrical', 'Civil', 'Chemical', 'Industrial', 'Chemistry','Auditor', 'Actuary', 'Banking', 'Research']         
  ```
- Standardized 29,212 job titles into **100 clusters** using:
    1. **Sentence embeddings** (`sentence-transformers/all-MiniLM-L6-v2`) for semantic similarity.    
    2. **KMeans clustering** to consolidate similar roles.    
    3. Named each cluster based on the most representative job title from the centroid.    
- Extracted **skills per job cluster** using a **SpaCy-based Hugging Face skill extractor**(this is a transformer trained on job skills data), sourcing nouns and verbs relative to job skills for high-level feature extraction.   
- Selected the **most relevant skills** per cluster based on frequency across all job descriptions within the cluster.
### 3. Exploratory Data Analysis (EDA)
 - Conducted initial EDA in a separate notebook to understand trends and distributions across STEM job postings. 
### 4. Interactive Dashboard
- Built a **Streamlit dashboard** to allow dynamic exploration of the engineered job clusters
	Features include:
	- **Select from 100 engineered STEM job clusters**.
	- **Top 30 skills** per cluster.
	- **Top N industries** hiring for a selected role.
	- **Top N companies** hiring for a selected role.
	- **Top N company specialities** hiring for a selected role.
    

> 	⚡ **Highlight:** The job title engineering and clustering is custom-built, condensing tens of thousands of titles into meaningful clusters, enabling better skill and hiring trend analysis.
## How to Run

1. Clone the repository:
	```
	git clone <your-repo-url>
	cd <your-repo-folder>
	```
2. Install dependencies:
	```
	pip install -r requirements.txt
	```
3. Launch the Streamlit dashboard:
 ```
streamlit run streamlit-app.py
 ```
## Technologies Used
- Python 3
- Pandas, NumPy
- SpaCy & Hugging Face Transformers
- SentenceTransformers (MiniLM-L6-v2)
- Scikit-learn (KMeans clustering)    
- Streamlit (interactive dashboard)
- SQLite (database for structured querying)
## Notebooks and Scripts
1. `data_ingestion.ipynb` – Explore CSV files, create SQLite database.
2. `feature_engineering.ipynb` – Job title clustering, skill extraction.
3. `eda.ipynb` – Initial exploratory data analysis.
4. `streamlit-app.py` – Interactive Streamlit dashboard.