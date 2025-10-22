--
-- PostgreSQL database dump
--

\restrict XeunAczrCHoZO66bp4bgZMxH75r21we8zLs68iXMfJq7RlSg49jY7AzR5gyyRZK

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies (
    company_id integer NOT NULL,
    name text,
    description text,
    company_size real,
    state text,
    country text,
    city text,
    zip_code text,
    address text,
    url text
);


ALTER TABLE public.companies OWNER TO postgres;

--
-- Name: company_industries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_industries (
    company_id integer,
    industry text
);


ALTER TABLE public.company_industries OWNER TO postgres;

--
-- Name: company_specialities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_specialities (
    company_id integer,
    speciality text
);


ALTER TABLE public.company_specialities OWNER TO postgres;

--
-- Name: employee_count; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_count (
    company_id integer,
    employee_count integer,
    follower_count integer,
    time_recorded integer
);


ALTER TABLE public.employee_count OWNER TO postgres;

--
-- Name: industries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.industries (
    industry_id integer NOT NULL,
    industry_name text
);


ALTER TABLE public.industries OWNER TO postgres;

--
-- Name: job_industries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_industries (
    job_id integer,
    industry_id integer
);


ALTER TABLE public.job_industries OWNER TO postgres;

--
-- Name: job_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_skills (
    job_id integer,
    skill_abr text
);


ALTER TABLE public.job_skills OWNER TO postgres;

--
-- Name: positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.positions (
    job_id integer NOT NULL,
    company_name text,
    title text,
    description text,
    location text,
    company_id integer,
    views real,
    formatted_work_type text,
    original_listed_time real,
    job_posting_url text,
    application_type text,
    expiry real,
    listed_time real,
    sponsored integer,
    work_type text,
    stem_match boolean,
    cluster_id integer,
    cluster_name text,
    clean_desc text,
    cluster_skills text
);


ALTER TABLE public.positions OWNER TO postgres;

--
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    skill_abr text NOT NULL,
    skill_name text
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (company_id);


--
-- Name: industries industries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.industries
    ADD CONSTRAINT industries_pkey PRIMARY KEY (industry_id);


--
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (job_id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (skill_abr);


--
-- Name: company_industries company_industries_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_industries
    ADD CONSTRAINT company_industries_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- Name: company_specialities company_specialities_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_specialities
    ADD CONSTRAINT company_specialities_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- Name: employee_count employee_count_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_count
    ADD CONSTRAINT employee_count_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- Name: job_industries job_industries_industry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_industries
    ADD CONSTRAINT job_industries_industry_id_fkey FOREIGN KEY (industry_id) REFERENCES public.industries(industry_id);


--
-- Name: job_industries job_industries_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_industries
    ADD CONSTRAINT job_industries_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.positions(job_id);


--
-- Name: job_skills job_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.positions(job_id);


--
-- Name: job_skills job_skills_skill_abr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_skill_abr_fkey FOREIGN KEY (skill_abr) REFERENCES public.skills(skill_abr);


--
-- Name: positions positions_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- PostgreSQL database dump complete
--

\unrestrict XeunAczrCHoZO66bp4bgZMxH75r21we8zLs68iXMfJq7RlSg49jY7AzR5gyyRZK

