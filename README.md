# Clinical Trial Landscape Analysis

### Exploring Clinical Research Trends Using Python and Power BI

## Project Overview

This project explores the clinical trial landscape using publicly available study records from [ClinicalTrials.gov](https://clinicaltrials.gov/).

Developed as part of a certified 543-hour Data Science training programme at DBE Academy, the project demonstrates an end-to-end analytical workflow, from automated data acquisition and preparation to exploratory data analysis and interactive visualization.

The analysis focuses on **5,000 clinical trial records** and examines study characteristics, enrollment patterns, therapeutic indications, funding sources, and temporal trends.

## Objectives

- Retrieve structured clinical trial data using the ClinicalTrials.gov API.
- Clean, transform, and validate clinical research datasets.
- Explore trial characteristics, study phases, and enrollment distributions.
- Identify frequently investigated medical conditions.
- Examine funding sources and study timelines.
- Develop an interactive Power BI dashboard to communicate analytical findings.

## Data Source

**Source:** ClinicalTrials.gov

**Dataset:** 5,000 clinical trial records

**Unique study identifiers:** 5,000 NCT IDs

**Data acquisition:** ClinicalTrials.gov API

The dataset includes information on trial registration identifiers, study titles, recruitment status, study phases, enrollment, medical conditions, interventions, sponsors, funding types, and study dates.

**Note:** The dataset represents a retrieved sample of clinical trial records rather than the entire ClinicalTrials.gov registry. Findings should therefore be interpreted as descriptive patterns within the analyzed dataset.

## Technologies and Tools

| Technology | Application |
|---|---|
| Python | Data extraction, cleaning and exploratory analysis |
| pandas | Data manipulation and transformation |
| Jupyter Notebook | Interactive analysis and documentation |
| Matplotlib | Statistical and exploratory visualizations |
| Power BI | Interactive dashboards and reporting |
| ClinicalTrials.gov API | Automated retrieval of clinical trial records |
| Git / GitHub | Version control and project documentation |

## Analytical Workflow

### 1. Data Acquisition

Retrieved clinical trial records programmatically through the ClinicalTrials.gov API.

The workflow supports structured extraction of study information for downstream analysis.

### 2. Data Cleaning and Preparation

Data preparation included:

- Inspecting data types and dataset structure.
- Checking missing values and duplicate study identifiers.
- Converting study dates into appropriate formats.
- Deriving study start years.
- Preparing enrollment data for statistical analysis.
- Separating multiple medical conditions for frequency analysis.
- Preparing structured datasets for visualization.

### 3. Exploratory Data Analysis

The analysis investigated:

**Clinical Trial Phases:** Distribution of studies across reported trial phases.

**Medical Conditions:** Frequently investigated disease indications and clinical conditions.

**Enrollment:** Distribution of participant enrollment and identification of unusually large studies.

**Funding Sources:** Representation of different funding categories.

**Temporal Trends:** Distribution of studies by reported start year.

**Study Status:** Comparison of enrollment characteristics across recruitment and completion statuses.

### 4. Data Quality Assessment

The dataset was assessed for missing values, record uniqueness, and field completeness.

Key observations included:

- 5,000 unique NCT identifiers across 5,000 records.
- 4,203 records without posted study results.
- 3,408 records without reported phase information.
- 3,395 records without collaborator information.

Missing phase information does not necessarily indicate poor data quality, as trial phases may not apply to certain study types.

Similarly, the absence of posted study results should not automatically be interpreted as a reporting violation.

## Power BI Dashboard

An interactive Power BI dashboard was developed to communicate clinical trial characteristics and analytical findings.

The dashboard includes visualizations of study phases, medical conditions, enrollment distributions, funding sources, and study start years.

**Dashboard preview:** Screenshot to be added.

## Project Structure

The repository is organized around the data acquisition scripts, analysis notebooks, dashboard files, and supporting documentation.

A detailed directory structure will be added once the final project files are uploaded.

## Limitations

- The dataset is a sample of ClinicalTrials.gov records and may not represent the full registry.
- Registry records can change over time.
- Missing fields may reflect study type, reporting requirements, or incomplete information.
- Enrollment values may be actual or estimated.
- Descriptive analyses do not establish causal relationships.

## Future Improvements

Potential extensions include:

- Expanding the dataset and documenting the retrieval strategy.
- Developing automated data refresh workflows.
- Adding interactive filters for trial phases, conditions, and funding sources.
- Exploring more advanced statistical and predictive methods.
- Integrating additional publicly available clinical research datasets.

## Author

**Manfred Anim, PhD**

Molecular Medicine | Translational Immunology | Genomics | Data Science

GitHub: [kwakuanim](https://github.com/kwakuanim)

## Acknowledgment

Developed as part of the certified Data Scientist training programme at DBE Academy.

## Data Attribution

Clinical trial information was obtained from the publicly accessible ClinicalTrials.gov database, maintained by the U.S. National Library of Medicine.

This project is intended for educational and portfolio purposes.# clinical-trial-landscape-analysis
Exploratory analysis and visualization of 5,000 clinical trials using Python and Power BI
