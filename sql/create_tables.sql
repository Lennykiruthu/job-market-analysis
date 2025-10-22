-- Create companies table
CREATE TABLE public.companies
(
  company_id INTEGER PRIMARY KEY,
  name TEXT,
  description TEXT,
  company_size REAL,
  state TEXT,
  country TEXT,
  city TEXT,
  zip_code TEXT,
  address TEXT,
  url TEXT
);

-- Create skills table
CREATE TABLE public.skills
(
  skill_abr TEXT PRIMARY KEY,
  skill_name TEXT
);

-- Create industries table
CREATE TABLE public.industries
(
  industry_id INTEGER PRIMARY KEY,
  industry_name TEXT
);

-- Create positions table
CREATE TABLE public.positions
(
  job_id INTEGER PRIMARY KEY,
  company_name TEXT,
  title TEXT,
  description TEXT,
  location TEXT,
  company_id INTEGER,
  views REAL,
  formatted_work_type TEXT,
  original_listed_time REAL,
  job_posting_url TEXT,
  application_type TEXT,
  expiry REAL,
  listed_time REAL,
  sponsored INTEGER,
  work_type TEXT,
  stem_match BOOLEAN,
  cluster_id INTEGER,
  cluster_name TEXT,
  clean_desc TEXT,
  cluster_skills TEXT,
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Create company_industries table
CREATE TABLE public.company_industries
(
  company_id INTEGER,
  industry TEXT,
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);


-- Create company_specialities table
CREATE TABLE public.company_specialities
(
  company_id INTEGER,
  speciality TEXT,
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Create employee_count table
CREATE TABLE public.employee_count
(
  company_id INTEGER,
  employee_count INTEGER,
  follower_count INTEGER,
  time_recorded INTEGER,
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Create job_skills table
CREATE TABLE public.job_skills
(
  job_id INTEGER,
  skill_abr TEXT,
  FOREIGN KEY (job_id) REFERENCES positions(job_id),
  FOREIGN KEY (skill_abr) REFERENCES skills(skill_abr)
);

-- Create job_skills table
CREATE TABLE public.job_industries
(
  job_id INTEGER,
  industry_id INTEGER,
  FOREIGN KEY (job_id) REFERENCES positions(job_id),
  FOREIGN KEY (industry_id) REFERENCES industries(industry_id)
);

