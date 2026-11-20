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

**Data acquisition:** ClinicalTrials.gov API v2

**Dataset version:** November 2026

**Sampling approach:** Records were retrieved using API pagination and ordered by the most recent registry update date.

The dataset includes information on:

- NCT identifiers
- Study titles
- Recruitment status
- Medical conditions
- Interventions and intervention types
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
| NumPy | Numerical operations |
| Matplotlib | Statistical and exploratory visualizations |
| Seaborn | Statistical data visualization |
| Power BI | Interactive dashboards and reporting |
| ClinicalTrials.gov API | Automated clinical trial data retrieval |
| Git and GitHub | Version control and project documentation |

---

## Analytical Workflow

### 1. Data Acquisition

Clinical trial records were retrieved programmatically through the ClinicalTrials.gov API.

The extraction workflow included API requests, pagination, structured field extraction, and removal of duplicate NCT identifiers.

**Script:** `fetch_clinical_trials.py`

### 2. Data Validation

Data validation was incorporated to assess dataset consistency and completeness before processing.

Validation checks included:

- Verification of 5,000 unique NCT identifiers
- Confirmation of completed study status
- Confirmation of interventional study type
- Assessment of missing values
- Examination of enrollment values
- Detection of duplicate identifiers
- Verification of required dataset columns
- Inspection of intervention classifications

**Script:** `validate_clinical_trials.py`

### 3. Data Processing

The validated records were prepared for analysis through data cleaning and transformation.

The analytical workflow included:

- Inspecting dataset structure
- Preparing study dates
- Deriving study start years
- Processing categorical variables
- Preparing enrollment data
- Extracting and standardizing study conditions
- Generating cleaned datasets for analysis

**Script:** `process_clinical_trials.py`

### 4. Exploratory Data Analysis

Exploratory analysis was performed to investigate study characteristics, funding categories, enrollment patterns, and temporal distributions.

The analysis generated nine figures covering intervention classifications, study start years, enrollment, study phases, funding categories, and medical conditions.

**Script:** `explore_data.py`

### 5. Data Updates

A separate Python script coordinates the automated data retrieval, validation, processing, visualization, and Power BI data preparation workflow.

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

## Key Findings and Visualizations

The analysis examined 5,000 completed interventional clinical trials retrieved from ClinicalTrials.gov.

- **Enrollment:** The studies reported a combined enrollment of 2,425,863, with a median enrollment of 62 participants per trial.
- **Study phases:** Phase information was not reported for 3,424 studies (68.5%). Among studies with reported phases, Phase 2 (436) and Phase 1 (351) were the most common categories.
- **Funding:** The OTHER funding category accounted for 3,723 studies (74.5%), followed by INDUSTRY with 996 studies (19.9%).
- **Drug classification:** Drug interventions were identified in 1,530 studies (30.6%), while 3,470 studies (69.4%) were classified as non-drug trials.
- **Study conditions:** Anxiety (83) and obesity (70) were among the most frequently reported condition labels.
- **Temporal distribution:** Studies starting in 2025 were particularly prominent in the selected dataset.

**Interpretation:** The dataset comprises a selected sample of recently updated, completed interventional studies. Therefore, the observed distributions and temporal patterns should not be interpreted as representative of all clinical trials registered worldwide.

### 1. Drug vs. Non-Drug Clinical Trials

![Drug vs Non-Drug Clinical Trials](figures/Drug%20vs%20non%20drug.png)

Among the 5,000 analyzed studies:

| Classification | Number | Percentage |
|---|---:|---:|
| Drug trials | 1,530 | 30.6% |
| Non-drug trials | 3,470 | 69.4% |
| **Total** | **5,000** | **100%** |

Non-drug trials represented the larger proportion of the analyzed dataset.

The classification reflects the project's intervention-based grouping and should not automatically be interpreted as a regulatory classification.

---

### 2. Clinical Trials by Study Start Year

![Clinical Trials by Start Year](figures/Clinical%20trials%20by%20year.png)

The distribution of clinical trials by study start year showed a concentration of records with recent start dates.

The highest number of sampled studies occurred in 2025 (1,110), followed by 2024 (846) and 2026 (730).

This pattern reflects the temporal composition of the selected records and may be influenced by the registry update-based sampling strategy.

It should not be interpreted as a measure of overall clinical trial growth.

---

### 3. Median Enrollment by Study Start Year

![Median Enrollment](figures/Median%20enrollment.png)

Median enrollment varied across study start years.

Earlier years showed larger fluctuations, while more recent years displayed comparatively stable median enrollment values.

For studies starting in 2025 and 2026, the median enrollment was 60 participants in each year.

These observations should be interpreted cautiously because the number of sampled studies varies across years.

---

### 4. Clinical Trial Enrollment Distribution

![Enrollment Distribution](figures/Enrollment_distribution.png)

Participant enrollment varied substantially across the analyzed studies.

The distribution was strongly right-skewed, with most trials reporting relatively modest enrollment and a small number reporting exceptionally large enrollment values.

A logarithmic scale was used to improve visualization across the wide enrollment range.

The median enrollment was 62 participants, compared with a mean of approximately 485 participants.

This difference illustrates the influence of exceptionally large studies on the mean enrollment.

---

### 5. Distribution of Clinical Trials by Study Phase

![Study Phases](figures/Study%20phases.png)

The study phase distribution showed:

| Study Phase | Number of Trials |
|---|---:|
| Not Reported | 3,424 |
| Phase 2 | 436 |
| Phase 1 | 351 |
| Phase 3 | 324 |
| Phase 4 | 251 |
| Phase 1 / Phase 2 | 120 |
| Early Phase 1 | 56 |
| Phase 2 / Phase 3 | 38 |
| **Total** | **5,000** |

Approximately 68.5% of the analyzed records had no reported study phase.

The absence of phase information does not necessarily indicate incomplete reporting, as phase classifications are not applicable to all types of interventional studies.

---

### 6. Clinical Trials by Funding Classification

![Funding Classification](figures/Funding%20classification.png)

The distribution of clinical trials across funding categories showed:

| Funding Type | Number of Trials | Percentage |
|---|---:|---:|
| OTHER | 3,723 | 74.5% |
| INDUSTRY | 996 | 19.9% |
| OTHER_GOV | 144 | 2.9% |
| NIH | 78 | 1.6% |
| FED | 36 | 0.7% |
| NETWORK | 22 | 0.4% |
| INDIV | 1 | 0.02% |
| **Total** | **5,000** | **Approximately 100%** |

Percentages are rounded.

The OTHER classification accounted for the largest proportion of studies, followed by INDUSTRY.

These categories describe the lead sponsor's registry classification rather than the financial amounts invested in individual studies.

---

### 7. Drug vs. Non-Drug Trials by Funding Category

![Drug Trials by Funding Category](figures/Drug%20trials%20by%20funding%20category.png)

The proportion of drug and non-drug studies varied across funding categories.

Among the 996 industry-classified studies, 652 (65.5%) involved drug interventions.

In comparison, 789 of the 3,723 studies (21.2%) in the OTHER funding classification involved drug interventions.

This comparison illustrates how intervention classifications differ across funding groups within the selected dataset.

---

### 8. Funding Categories by Study Start Year

![Funding Over Time](figures/Funding%20over%20time.png)

The distribution of clinical trials across study start years showed a concentration of records in more recent years.

The OTHER funding classification accounted for the largest share across many study years.

Industry-classified studies also contributed to the observed distribution.

These patterns should be interpreted in the context of the dataset selection method rather than as evidence of registry-wide growth.

---

### 9. Most Frequent Conditions in Completed Clinical Trials

![Most Frequent Conditions](figures/Most%20frequent%20condition%20in%20completed%20trials.png)

The most frequently represented condition labels included:

| Condition | Number of Trials |
|---|---:|
| Anxiety | 83 |
| Obesity | 70 |
| Healthy | 64 |
| Stroke | 60 |
| Pain | 47 |
| Healthy Volunteers | 46 |
| Postoperative Pain | 45 |
| Depression | 43 |
| Breast Cancer | 39 |
| Hypertension | 39 |

Anxiety and obesity were the two most frequently reported condition labels in the analyzed sample.

Because individual trials may report multiple conditions, these counts are not mutually exclusive.

The condition categories reflect the terminology recorded in ClinicalTrials.gov and have not been comprehensively harmonized into standardized medical concepts.

---

## Data Quality Assessment

Data quality assessment formed an important component of the analytical workflow.

The analysis included:

- Examination of missing values
- Verification of unique NCT identifiers
- Confirmation of completed interventional study status
- Review of study phase completeness
- Assessment of enrollment information
- Inspection of categorical variables
- Preparation of date fields for analysis
- Verification of intervention-type availability

The dataset contained 5,000 unique NCT identifiers across 5,000 records.

All 5,000 records had enrollment values, intervention-type information, and valid study start years after processing.

Study phase information was not reported for 3,424 records.

Missing or non-applicable values were also observed in several variables, including collaborators and posted study results.

These observations highlight the importance of considering registry reporting requirements and study characteristics when interpreting clinical trial datasets.

---

## Repository Structure

```text
clinical-trial-landscape-analysis/
│
├── Data/
│   ├── README.md
│   ├── clinical_trials_full_5000.csv
│   ├── clinical_trials_cleaned_5000.csv
│   ├── clinical_trial_conditions_5000.csv
│   ├── clinical_trials_cleaned.csv
│   └── clinical_trial_conditions.csv
│
├── figures/
│   ├── Power BI dashboard.png
│   ├── Drug vs non drug.png
│   ├── Clinical trials by year.png
│   ├── Median enrollment.png
│   ├── Enrollment_distribution.png
│   ├── Study phases.png
│   ├── Funding classification.png
│   ├── Drug trials by funding category.png
│   ├── Funding over time.png
│   ├── Most frequent condition in completed trials.png
│   └── Intervention.png
│
├── Clinical_Trial_Analysis_5000.pbix
├── LICENSE
├── README.md
├── requirements.txt
├── fetch_clinical_trials.py
├── validate_clinical_trials.py
├── process_clinical_trials.py
├── explore_data.py
└── update_clinical_trials.py
```

The additional `Intervention.png` file is retained in the figures directory but is not included in the nine analytical findings above.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kwakuanim/clinical-trial-landscape-analysis.git

cd clinical-trial-landscape-analysis
```

### 2. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Validate the Existing Dataset

The repository contains the raw and processed datasets used for the analysis.

To validate the existing raw dataset without retrieving new records, run:

```bash
python validate_clinical_trials.py
```

### 4. Process the Clinical Trial Data

To regenerate the cleaned datasets and extracted condition records, run:

```bash
python process_clinical_trials.py
```

### 5. Generate the Analytical Figures

To reproduce the nine analytical figures, run:

```bash
python explore_data.py
```

The generated figures are saved in the `figures/` directory.

### 6. Retrieve Updated Clinical Trial Data (Optional)

To retrieve a new dataset from ClinicalTrials.gov, run:

```bash
python fetch_clinical_trials.py
```

**Important:** This command replaces the existing raw dataset. Since records are ordered by their latest update date, a new retrieval may produce different studies and analytical results.

After retrieval, repeat the validation, processing, and visualization steps.

### 7. Automated Pipeline (Optional)

The project includes an automated workflow script:

```bash
python update_clinical_trials.py --refresh
```

This command is intended to execute the complete retrieval, validation, processing, visualization, and Power BI CSV update workflow.

**Note:** The individual validation, processing, and visualization scripts have been tested successfully against the existing dataset. The complete automated pipeline has not yet been independently tested from a fresh installation.

### 8. Explore the Power BI Dashboard

Open the following file using Microsoft Power BI Desktop:

`Clinical_Trial_Analysis_5000.pbix`

The Power BI file may require its local CSV source paths to be updated after cloning the repository.

---

## Project Limitations

The analysis has several limitations:

1. **Sampling:** The dataset represents selected recently updated completed interventional studies rather than the entire ClinicalTrials.gov registry.
2. **Data completeness:** Certain variables contain missing or non-applicable values.
3. **Enrollment:** Reported enrollment reflects registry values and does not establish a deduplicated participant count across studies.
4. **Temporal interpretation:** Study start-year patterns may be influenced by the sampling approach.
5. **Classification:** Drug and non-drug categories follow the project's analytical classification method.
6. **Funding:** Funding categories reflect the lead sponsor's classification and do not represent verified funding amounts.
7. **Condition terminology:** Condition labels are based on registry entries and may contain overlapping or differently worded concepts.
8. **Causality:** The findings are descriptive and do not establish causal relationships.

---

## Future Improvements

Potential extensions include:

- Expanding the clinical trial dataset.
- Implementing scheduled automated data refresh workflows.
- Improving documentation and testing of the complete analytical pipeline.
- Introducing automated data validation tests.
- Expanding Power BI filtering and analytical capabilities.
- Investigating clinical trial characteristics across therapeutic areas.
- Exploring advanced statistical and predictive analytical methods.

---

## Author

**Manfred Anim, PhD**

Molecular Medicine | Translational Immunology | Genomics | Data Science

**GitHub:** [kwakuanim](https://github.com/kwakuanim)

**Professional Interests:**

Biomedical Data Science, Bioinformatics, Clinical Research Analytics, Translational Medicine, and Precision Medicine.

---

## Acknowledgment

This project was developed as part of the certified **Data Scientist training programme at DBE Academy (2026)**.

The programme comprised 543 teaching hours covering Python, R, database technologies, artificial intelligence, machine learning, data visualization, cloud computing, and practical project development.

---

## Data Attribution

Clinical trial information was obtained from [ClinicalTrials.gov](https://clinicaltrials.gov/), maintained by the U.S. National Library of Medicine.

API documentation: https://clinicaltrials.gov/data-api/api

This project is intended for educational, research, and professional portfolio purposes.
