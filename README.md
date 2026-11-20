# Clinical Trial Landscape Analysis

**Exploratory Analysis and Visualization of 5,000 Clinical Trials Using Python and Power BI**

## Project Overview

This project explores clinical trial characteristics and research patterns using publicly available data retrieved from [ClinicalTrials.gov](https://clinicaltrials.gov/).

Developed as part of a certified **543-hour Data Science training programme at DBE Academy**, the project demonstrates data extraction, cleaning, exploratory data analysis, and visualization techniques applied to clinical research data.

The analysis examines **5,000 clinical trial records**, focusing on study classifications, funding sources, study phases, medical conditions, participant enrollment, and study start years.

The project combines computational data analysis with a biomedical research perspective to explore patterns within clinical trial datasets.

> **Scope:** The findings describe the analyzed sample of 5,000 records and should not be generalized to the entire ClinicalTrials.gov registry.

---

## Project Objectives

- Retrieve clinical trial records programmatically using the ClinicalTrials.gov API.
- Clean, transform, and prepare structured datasets for analysis.
- Examine drug versus non-drug clinical trial classifications.
- Investigate clinical trial funding patterns.
- Analyze study phases and frequently investigated medical conditions.
- Explore participant enrollment distributions and temporal patterns.
- Develop visualizations to communicate findings from clinical research data.

---

## Data Source

**Source:** ClinicalTrials.gov

**Dataset size:** 5,000 clinical trial records

**Unique study identifiers:** 5,000 NCT IDs

**Data acquisition:** ClinicalTrials.gov API

The dataset includes study identifiers, titles, recruitment status, medical conditions, interventions, study phases, enrollment, sponsors, funding classifications, and study dates.

The dataset represents a sample of registered clinical studies retrieved from ClinicalTrials.gov, not the complete database.

---

## Technologies and Tools

| Technology | Application |
|---|---|
| Python | Data extraction, processing and exploratory analysis |
| pandas | Data cleaning, manipulation and transformation |
| Matplotlib | Statistical and exploratory visualizations |
| Jupyter Notebook | Interactive data analysis |
| Power BI | Dashboard development and reporting |
| ClinicalTrials.gov API | Automated retrieval of clinical trial records |
| Git / GitHub | Version control and project documentation |

---

## Analytical Workflow

### 1. Data Acquisition

Clinical trial records were retrieved programmatically through the ClinicalTrials.gov API.

The retrieved dataset was organized into structured fields for downstream processing and analysis.

### 2. Data Cleaning and Preparation

Data preparation involved:

- Examining dataset dimensions and variable types.
- Checking missing values and duplicate study identifiers.
- Converting study dates into appropriate formats.
- Extracting study start years.
- Preparing enrollment variables for statistical analysis.
- Processing medical condition fields.
- Preparing datasets for exploratory analysis and visualization.

### 3. Exploratory Data Analysis

The analysis investigated trial classifications, funding sources, study phases, medical conditions, enrollment distributions, and temporal patterns.

---
## Interactive Power BI Dashboard

An interactive Power BI dashboard was developed to explore and communicate clinical trial characteristics using a dataset of 5,000 completed interventional studies retrieved from ClinicalTrials.gov.

![Clinical Trial Analysis Power BI Dashboard](figures/power_bi_dashboard.png)

### Dashboard Features

The dashboard provides an overview of:

- **Clinical Trial Overview:** 5,000 clinical trial records, total reported enrollment of 2,624,083 participants, and median enrollment of 62.
- **Study Phase Distribution:** Comparison of clinical trials across reported study phases.
- **Funding Classification:** Distribution of studies across industry, government, NIH, and other funding categories.
- **Medical Conditions:** Visualization of frequently investigated clinical conditions.
- **Enrollment Trends:** Median participant enrollment by study start year.
- **Temporal Trends:** Distribution of clinical trials according to study start year.

### Interactive Functionality

The dashboard includes interactive filters for:

- Study start date
- Funding classification

These features allow users to explore subsets of the dataset and examine differences in clinical trial characteristics.

### Analytical Value

The dashboard integrates data preparation, exploratory analysis, and business intelligence visualization to communicate findings from clinical research data.

**Tools:** Python, pandas, Matplotlib, Power BI.
## Key Findings and Visualizations

### 1. Drug vs. Non-Drug Clinical Trials

![Drug vs Non-Drug Clinical Trials](figures/drug_vs_non_drug_donut.png)

Of the 5,000 clinical trial records:

- **1,556 trials (31.1%)** were classified as drug trials.
- **3,444 trials (68.9%)** were classified as non-drug trials.

Non-drug trials represented the larger proportion of studies within the analyzed dataset.

These classifications follow the project's analytical classification method and should not automatically be interpreted as regulatory classifications.

### 2. Clinical Trials by Funding Classification

![Clinical Trials by Funding Classification](figures/funder_type_distribution.png)

The distribution of clinical trials across funding categories showed:

| Funding classification | Percentage |
|---|---:|
| OTHER | 74.5% |
| INDUSTRY | 19.7% |
| OTHER_GOV | 2.9% |
| NIH | 1.6% |
| FED | 0.7% |
| NETWORK | 0.5% |
| INDIV | 0.0% |

*Percentages are rounded.*

The `OTHER` classification accounted for the largest proportion of studies, followed by industry-funded studies.

These categories represent registry funder classifications rather than direct measures of financial investment.

### 3. Drug vs. Non-Drug Trials by Funding Category

![Drug vs Non-Drug Trials by Funding Category](figures/funding_drug_non_drug.png)

The distribution of drug and non-drug trials varied across funding classifications.

Industry-funded studies had a higher proportion of drug trials than the other major funding categories, whereas non-drug trials predominated in several non-industry categories.

This analysis demonstrates how intervention classifications can be compared across funding groups.

### 4. Clinical Trials by Funding Type and Study Start Year

![Clinical Trials by Funding Type and Study Start Year](figures/funding_stacked_barplot.png)

The distribution of study start years showed a concentration of trial records in more recent years.

The `OTHER` funding classification accounted for the largest share across many study years, with industry-funded studies also contributing substantially.

The apparent increase in trial counts should be interpreted within the context of the dataset's retrieval and sampling strategy rather than as evidence of registry-wide growth.

### 5. Distribution of Clinical Trial Enrollment

![Clinical Trial Enrollment Distribution](figures/enrollment_distribution.png)

Participant enrollment varied substantially across clinical trials.

Most studies had relatively modest enrollment sizes, while a small number of exceptionally large studies produced a strongly right-skewed distribution.

A logarithmic scale was used to improve visualization across the wide range of enrollment values.

This analysis illustrates the importance of examining distributional characteristics when working with clinical research datasets.

### 6. Median Clinical Trial Enrollment by Start Year

![Median Clinical Trial Enrollment by Start Year](figures/median_enrollment_by_year.png)

Median enrollment varied across study start years.

Earlier years displayed greater fluctuations, while more recent years showed comparatively stable median enrollment values.

For studies starting in **2025 and 2026**, the plotted median enrollment was approximately **60 participants**.

These patterns should be interpreted cautiously because the number and characteristics of sampled studies vary across years.

### 7. Distribution of Clinical Trials by Study Phase

![Distribution of Clinical Trials by Study Phase](figures/reported_study_phases.png)

The distribution of reported study phases revealed that:

- **3,399 studies (68.0%)** had no reported phase.
- Phase 2 accounted for 448 records.
- Phase 1 accounted for 352 records.
- Phase 3 accounted for 333 records.
- Phase 4 accounted for 259 records.

Additional studies were classified under combined or early-phase categories.

The absence of phase information does not necessarily indicate incomplete reporting, since phase classifications are not applicable to all study types.

### 8. Top 10 Conditions in Completed Clinical Trials

![Top 10 Conditions in Completed Clinical Trials](figures/top_10_conditions.png)

The most frequently reported condition labels among completed clinical trials included:

| Condition | Number of trials |
|---|---:|
| Anxiety | 85 |
| Obesity | 74 |
| Healthy | 72 |
| Stroke | 61 |
| Depression | 50 |
| Postoperative Pain | 50 |
| Pain | 43 |
| Breast Cancer | 40 |
| Healthy Volunteers | 39 |
| Hypertension | 38 |

Anxiety and obesity were among the most frequently represented conditions in the completed-trial subset.

A single trial may report multiple conditions. Therefore, condition counts should not be interpreted as mutually exclusive study counts.

### 9. Clinical Trials by Study Start Year

![Clinical Trials by Study Start Year](figures/clinical_trials_by_year.png)

The distribution of clinical trials by study start year revealed a concentration of records with recent start dates.

The highest number of records occurred in **2025**, followed by a lower count for 2026.

These findings reflect the temporal composition of the analyzed sample and may be influenced by the data retrieval strategy.

---

## Data Quality Assessment

Data quality assessment was incorporated into the analytical workflow to evaluate dataset completeness and consistency.

The analysis included:

- Checking missing values.
- Verifying unique clinical trial identifiers.
- Examining variable completeness.
- Reviewing enrollment data.
- Identifying fields requiring transformation or further interpretation.

The dataset contained **5,000 unique NCT identifiers across 5,000 records**.

Missing values were observed in several variables, including study phases, collaborators, and posted study results.

These observations highlight the importance of considering study characteristics and reporting requirements when interpreting registry data.

---

## Repository Structure

```text
clinical-trial-landscape-analysis/
│
├── README.md
│
├── figures/
│   ├── drug_vs_non_drug_donut.png
│   ├── funder_type_distribution.png
│   ├── funding_drug_non_drug.png
│   ├── funding_stacked_barplot.png
│   ├── median_enrollment_by_year.png
│   ├── reported_study_phases.png
│   ├── top_10_conditions.png
│   ├── enrollment_distribution.png
│   └── clinical_trials_by_year.png
│
└── LICENSE
```

*Python scripts, analysis notebooks, and Power BI files can be added after review and preparation for public release.*

---

## Limitations

Several limitations should be considered when interpreting the findings:

1. **Sampling:** The dataset represents a sample of ClinicalTrials.gov records rather than the entire registry.
2. **Data completeness:** Some variables contain missing or non-applicable information.
3. **Enrollment:** Participant enrollment may represent actual or estimated values depending on the study.
4. **Temporal patterns:** Differences across study start years may be influenced by sampling and registry updates.
5. **Classification:** Drug and non-drug categories follow the project's analytical classification method.
6. **Interpretation:** The analyses are descriptive and do not establish causal relationships.

---

## Future Improvements

Potential extensions of the project include:

- Expanding the clinical trial dataset.
- Implementing automated data refresh workflows.
- Developing additional interactive Power BI visualizations.
- Examining clinical trial characteristics across therapeutic areas.
- Investigating relationships between funding classifications, study phases, and enrollment.
- Exploring advanced statistical and machine learning approaches.

---

## Author

**Manfred Anim, PhD**

Molecular Medicine | Translational Immunology | Genomics | Data Science

**GitHub:** [kwakuanim](https://github.com/kwakuanim)

**Professional Interests:** Biomedical Data Science, Bioinformatics, Clinical Research Analytics, Translational Medicine and Precision Medicine.

---

## Acknowledgment

This project was developed as part of the certified **Data Scientist training programme at DBE Academy (2026)**.

The programme comprised 543 teaching hours covering programming, data science, database technologies, artificial intelligence, machine learning, cloud computing, data visualization, and practical project development.

---

## Data Attribution

Clinical trial information was obtained from [ClinicalTrials.gov](https://clinicaltrials.gov/), maintained by the U.S. National Library of Medicine.

This project is intended for educational, research, and portfolio purposes.
