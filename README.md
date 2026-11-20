# Clinical Trial Landscape Analysis

### Exploring Clinical Trial Characteristics, Enrollment, and Funding Trends Using Python and Power BI

**Data Science Portfolio Project | DBE Academy | November 2026**

![Clinical Trial Analysis Dashboard](figures/Power%20BI%20dashboard.png)

## Project Overview

This project explores clinical trial characteristics and research patterns using publicly available data retrieved from [ClinicalTrials.gov](https://clinicaltrials.gov/).

Developed as part of a certified **543-hour Data Science training programme at DBE Academy**, the project demonstrates the practical application of Python programming, API-based data extraction, data cleaning, exploratory data analysis, data visualization, and interactive dashboard development.

The analysis focuses on **5,000 completed interventional clinical studies**, examining:

- Drug versus non-drug intervention classifications
- Clinical trial funding sources
- Study phase distributions
- Medical conditions investigated
- Participant enrollment patterns
- Study start years and temporal distributions

The project combines computational data analysis with a biomedical research perspective to explore patterns in clinical trial datasets.

**Important:** Findings describe the selected sample of 5,000 studies and should not be generalized to the entire ClinicalTrials.gov registry.

---

## Project Objectives

The main objectives were to:

1. Retrieve structured clinical trial records using the ClinicalTrials.gov API.
2. Clean, transform, and validate clinical research data.
3. Explore drug and non-drug clinical trial classifications.
4. Investigate study phases and funding categories.
5. Identify frequently investigated medical conditions.
6. Examine participant enrollment distributions.
7. Explore study start-year patterns.
8. Develop an interactive Power BI dashboard to communicate analytical findings.

---

## Data Source and Sampling

**Source:** [ClinicalTrials.gov](https://clinicaltrials.gov/)

**Dataset:** 5,000 clinical trial records

**Unique study identifiers:** 5,000 NCT IDs

**Study selection:** Completed interventional studies

**Data acquisition:** ClinicalTrials.gov API

**Dataset version:** November 2026

**Sampling approach:** Records were retrieved using API pagination and ordered by the most recent registry update date.

The dataset includes information on:

- NCT identifiers
- Study titles
- Recruitment status
- Medical conditions
- Interventions
- Study phases
- Participant enrollment
- Sponsors and funding classifications
- Study start and completion dates

Because the dataset consists of selected recently updated records, it should not be interpreted as a representative sample of the complete registry.

---

## Technologies and Tools

| Technology | Application |
|---|---|
| Python | API retrieval, data processing, and exploratory analysis |
| pandas | Data cleaning, manipulation, and transformation |
| Matplotlib | Statistical and exploratory visualizations |
| Power BI | Interactive dashboards and reporting |
| ClinicalTrials.gov API | Automated clinical trial data retrieval |
| Git and GitHub | Version control and project documentation |

---

## Analytical Workflow

### 1. Data Acquisition

Clinical trial records were retrieved programmatically through the ClinicalTrials.gov API.

The extraction workflow included API requests, pagination, structured field extraction, and removal of duplicate NCT identifiers.

**Script:** `fetch_clinical_trials.py`

### 2. Data Processing

The retrieved records were prepared for analysis through data cleaning and transformation.

The analytical workflow included:

- Inspecting dataset structure
- Checking missing values
- Reviewing duplicate identifiers
- Preparing study dates
- Deriving study start years
- Processing categorical variables
- Preparing enrollment data

**Script:** `process_clinical_trials.py`

### 3. Data Validation

Data validation was incorporated to assess dataset consistency and completeness.

Validation checks included examining missing values, reviewing enrollment distributions, and verifying unique NCT identifiers.

**Script:** `validate_clinical_trials.py`

### 4. Exploratory Data Analysis

Exploratory analysis was performed to investigate study characteristics, funding categories, enrollment patterns, and temporal distributions.

**Script:** `explore_data.py`

### 5. Data Updates

A separate Python script supports the project's data update workflow.

**Script:** `update_clinical_trials.py`

### 6. Data Visualization and Reporting

Python visualizations were created to communicate analytical findings.

An interactive Power BI dashboard was also developed to present study characteristics and allow further exploration of the dataset.

---

## Interactive Power BI Dashboard

The dashboard provides an overview of clinical trial characteristics using interactive visualizations and filtering options.

### Dashboard Summary

| Indicator | Value |
|---|---:|
| Total clinical trials | 5,000 |
| Total reported enrollment | 2,425,863 |
| Median enrollment | 62 |

Total enrollment is the sum of reported study enrollment values, not a verified count of unique participants across studies.

### Dashboard Features

The dashboard includes:

- Clinical trial phase distribution
- Clinical trials by funding classification
- Frequently investigated medical conditions
- Median enrollment by study start year
- Clinical trials by start year
- Interactive study start-date filtering
- Interactive funding classification filtering

**Power BI File:** [Clinical_Trial_Analysis_5000.pbix](Clinical_Trial_Analysis_5000.pbix)

---

# Key Findings and Visualizations

The analysis examined 5,000 completed interventional clinical trials retrieved from ClinicalTrials.gov.

- **Enrollment:** The studies reported a combined enrollment of 2,425,863 participants, with a median enrollment of 62 participants per trial.
- **Study phases:** Phase information was not reported for 3,424 studies (68.5%). Among studies with reported phases, Phase 2 (436) and Phase 1 (351) were the most common categories.
- **Funding:** The OTHER funding category accounted for 3,723 studies (74.5%), followed by INDUSTRY with 996 studies (19.9%).
- **Drug classification:** Drug interventions were identified in 1,530 studies (30.6%), while 3,470 studies (69.4%) were classified as non-drug trials.
- **Study conditions:** Anxiety and obesity were among the most frequently reported conditions.
