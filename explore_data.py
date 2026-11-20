import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns

# Load the cleaned clinical trial dataset
df = pd.read_csv("Data/clinical_trials_cleaned_5000.csv")

# Check the dataset
print("Total clinical trials:", len(df))
print("Dataset columns:", df.shape[1])

# Create directory for figures
Path("figures").mkdir(exist_ok=True)


# Count studies by phase
phase_counts = (
    df["Phases"]
    .fillna("Not Reported")
    .value_counts()
    .sort_values(ascending=True)
)

# Set a clean scientific style
sns.set_theme(style="whitegrid", context="talk")

# Create figure
fig, ax = plt.subplots(figsize=(11, 6.5))

# Use different colours for each phase
colors = sns.color_palette("viridis", n_colors=len(phase_counts))

bars = ax.barh(
    phase_counts.index,
    phase_counts.values,
    color=colors,
    height=0.7
)

# Add count labels
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + max(phase_counts) * 0.012,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

# Title and axis labels
ax.set_title(
    "Distribution of Clinical Trials by Study Phase",
    fontsize=17,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Number of Clinical Trials", fontsize=12)
ax.set_ylabel("Study Phase", fontsize=12)

# Light gridlines only on the x-axis
ax.grid(axis="x", linestyle="--", alpha=0.25)
ax.grid(axis="y", visible=False)

# Remove unnecessary borders
sns.despine(left=True, bottom=True)

# Leave space for labels
ax.set_xlim(0, phase_counts.max() * 1.15)

# Save figure
Path("figures").mkdir(exist_ok=True)

plt.tight_layout()
plt.savefig(
    "figures/reported_study_phases.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()




## Plot clinical trials with reported phases
# Select studies with reported phases
reported_phases = df["Phases"].dropna()



## Plot clinical trials with reported phases
# Select studies with reported phases
reported_phases = df["Phases"].dropna()

# Count studies in each phase
phase_counts_reported = reported_phases.value_counts()

# Set different colours for each study phase
colors = sns.color_palette("Set2", n_colors=len(phase_counts_reported))

# Create the bar chart
ax = phase_counts_reported.plot(
    kind="bar",
    figsize=(10, 6),
    color=colors,
    edgecolor="white",
    linewidth=1
)

# Add values above the bars
for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(
        f"{int(height):,}",
        (bar.get_x() + bar.get_width() / 2, height),
        ha="center",
        va="bottom",
        xytext=(0, 3),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold"
    )

# Title and axis labels
plt.title(
    f"Clinical Trials with Reported Study Phases (n={len(reported_phases):,})",
    fontsize=15,
    fontweight="bold",
    pad=20
)
plt.xlabel("Study Phase", fontsize=12)
plt.ylabel("Number of Clinical Trials", fontsize=12)
plt.xticks(rotation=45, ha="right")

# Improve the grid and remove unnecessary borders
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)
sns.despine()

# Leave space above bars for labels
ax.set_ylim(0, phase_counts_reported.max() * 1.15)

plt.tight_layout()

# Save the first chart
plt.savefig(
    "figures/study_phase_distribution.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


##explore clinical trails by disease
# Examine the most frequently reported conditions
print("\nTop 10 reported conditions:")
print(df["Conditions"].value_counts().head(10))

## How are multiple conditions stored
# Display the first 10 condition entries
print("\nFirst 10 condition entries:")
print(df["Conditions"].head(10).to_string(index=False))

## separate the different conditions
# Split multiple conditions into separate entries
conditions_df = df[["NCT Number", "Conditions"]].copy()

conditions_df["Conditions"] = (
    conditions_df["Conditions"]
    .fillna("")
    .str.split("|", regex=False)
)

# Create one row per condition
conditions_df = conditions_df.explode("Conditions")

# Remove extra spaces
conditions_df["Conditions"] = (
    conditions_df["Conditions"].str.strip())

# Remove empty entries
conditions_df = conditions_df[
    conditions_df["Conditions"] != ""]

# Count each condition once per clinical trial
conditions_df = conditions_df.drop_duplicates(
    subset=["NCT Number", "Conditions"])

# Count the 10 most frequent conditions
top_conditions = (
    conditions_df["Conditions"]
    .value_counts()
    .head(10))

print("\nTop 10 conditions after splitting:")
print(top_conditions)

# Set a different colour palette for medical conditions
colors = sns.color_palette("crest", n_colors=len(top_conditions))

# Plot the top 10 conditions
plt.close("all")

fig, ax = plt.subplots(figsize=(11, 6.5))

top_conditions.sort_values().plot(
    kind="barh",
    ax=ax,
    color=colors,
    edgecolor="white",
    linewidth=0.8
)
# Title and axis labels
plt.title(
    "Top 10 Conditions in Completed Clinical Trials",
    fontsize=16,
    fontweight="bold",
    pad=20
)
plt.xlabel("Number of Clinical Trials", fontsize=12)
plt.ylabel("Medical Condition", fontsize=12)

# Add counts at the end of each bar
for bar in ax.patches:
    width = bar.get_width()
    ax.annotate(
        f"{int(width):,}",
        (width, bar.get_y() + bar.get_height() / 2),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

# Improve gridlines and remove unnecessary borders
ax.grid(axis="x", linestyle="--", alpha=0.25)
ax.grid(axis="y", visible=False)
ax.set_axisbelow(True)
sns.despine(left=True, bottom=True)

# Leave space for count labels
plt.xlim(0, top_conditions.max() * 1.15)

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/top_10_conditions.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()



## Enrolment/participants in the study
##do studies have small or larger participants
# Descriptive statistics for enrollment
print("\nClinical Trial Enrollment Statistics:")
print(df["Enrollment"].describe())

## Visualize the enrollment distribution

import numpy as np

# Select positive enrollment values for logarithmic plotting
enrollment_positive = df["Enrollment"].dropna()
enrollment_positive = enrollment_positive[enrollment_positive > 0]

# Create logarithmically spaced bins
bins = np.logspace(
    np.log10(enrollment_positive.min()),
    np.log10(enrollment_positive.max()),
    30
)

# Plot enrollment distribution
fig, ax = plt.subplots(figsize=(11, 6.5))

ax.hist(
    enrollment_positive,
    bins=bins,
    color="#34699A",
    edgecolor="white",
    linewidth=0.8,
    alpha=0.9
)

plt.xscale("log")

# Title and axis labels
plt.title(
    "Distribution of Clinical Trial Enrollment",
    fontsize=16,
    fontweight="bold",
    pad=20
)
plt.xlabel("Number of Participants (Log Scale)", fontsize=12)
plt.ylabel("Number of Clinical Trials", fontsize=12)

# Improve gridlines
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

# Remove unnecessary borders
sns.despine()

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/enrollment_distribution.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


## Find largest studies 
# Identify the 10 studies with the highest enrollment
top_enrollment = df.nlargest(10, "Enrollment")

# Display selected columns
print("\nTop 10 Clinical Trials by Enrollment:")

print(
    top_enrollment[
        ["NCT Number", "Study Title", "Enrollment", "Phases"]
    ].to_string(index=False)
)

##clinical trends over time 
# Convert start dates into datetime format
# Convert dates using day/month/year format
# Convert mixed date formats
df["Start Date"] = pd.to_datetime(
    df["Start Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Extract the year
df["Start Year"] = df["Start Date"].dt.year

# Count studies by start year
trials_per_year = df["Start Year"].value_counts().sort_index()

print("\nClinical Trials by Start Year:")
print(trials_per_year.to_string())

##previously there were some missing years, which needed troubleshooting
#### checking for missing time dates
# Check missing start years
print("\nMissing Start Years:")
print(df["Start Year"].isna().sum())

# Display examples of missing start dates
print("\nExamples of unrecognized start dates:")
print(
    df.loc[df["Start Year"].isna(),
           ["NCT Number", "Start Date"]].head(10)
)


## check original dates
# Reload the original dataset
df_original = pd.read_csv("Data/ctg-studies.csv")

# Display original dates that failed conversion
print("\nOriginal Start Dates That Failed Conversion:")

print(
    df_original.loc[
        df["Start Year"].isna(),
        ["NCT Number", "Start Date"]
    ].head(15).to_string(index=False)
)


##plot 
# Count clinical trials by start year
trials_per_year = df["Start Year"].value_counts().sort_index()

# Create a line chart
fig, ax = plt.subplots(figsize=(11, 6.5))

ax.plot(
    trials_per_year.index,
    trials_per_year.values,
    marker="o",
    color="#7B2CBF",
    linewidth=2.5,
    markersize=7,
    markerfacecolor="white",
    markeredgecolor="#7B2CBF",
    markeredgewidth=2
)

# Title and axis labels
ax.set_title(
    "Clinical Trials by Start Year",
    fontsize=16,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Study Start Year", fontsize=12)
ax.set_ylabel("Number of Clinical Trials", fontsize=12)

# Display all study start years
ax.set_xticks(trials_per_year.index)
plt.xticks(rotation=45, ha="right")

# Improve gridlines
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

# Remove unnecessary borders
sns.despine()

# Start the y-axis at zero
ax.set_ylim(bottom=0)

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/clinical_trials_by_year.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


## Analyze enrollment by study start year
## How does the typical number of participants enrolled in clinical trials vary across study start years?
# Calculate median enrollment by study start year
median_enrollment_by_year = (
    df.groupby("Start Year")["Enrollment"]
    .median()
)

print("\nMedian Enrollment by Study Start Year:")
print(median_enrollment_by_year.to_string())


##Plot
# Plot median enrollment by start year
fig, ax = plt.subplots(figsize=(11, 6.5))

ax.plot(
    median_enrollment_by_year.index,
    median_enrollment_by_year.values,
    marker="o",
    color="#D97706",
    linewidth=2.5,
    markersize=7,
    markerfacecolor="white",
    markeredgecolor="#D97706",
    markeredgewidth=2
)

# Title and axis labels
ax.set_title(
    "Median Clinical Trial Enrollment by Start Year",
    fontsize=16,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Study Start Year", fontsize=12)
ax.set_ylabel("Median Number of Participants", fontsize=12)

# Display all study start years
ax.set_xticks(median_enrollment_by_year.index)
plt.xticks(rotation=45, ha="right")

# Improve gridlines
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

# Remove unnecessary borders
sns.despine()

# Start the y-axis at zero
ax.set_ylim(bottom=0)
# Add median enrollment values above each data point
for year, median in median_enrollment_by_year.items():
    ax.annotate(
        f"{median:,.0f}",
        (year, median),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color="#92400E"
    )

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/median_enrollment_by_year.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


##funding types
# Analyze clinical trial funding types
print("\nClinical Trials by Funder Type:")

funder_counts = df["Funder Type"].value_counts()

print(funder_counts.to_string())


##plot
# Calculate funding type percentages
funder_percentages = (
    df["Funder Type"].value_counts(normalize=True) * 100
)

# Set different colours for each funding category
colors = sns.color_palette(
    ["#2563A6", "#16A085", "#7E57C2", "#66A61E"],
    n_colors=len(funder_percentages)
)
# Create bar chart
fig, ax = plt.subplots(figsize=(10, 6.5))

bars = ax.bar(
    funder_percentages.index,
    funder_percentages.values,
    color=colors,
    edgecolor="white",
    linewidth=1,
    width=0.65
)

# Add percentage labels
for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(
        f"{height:.1f}%",
        (bar.get_x() + bar.get_width() / 2, height),
        ha="center",
        va="bottom",
        xytext=(0, 5),
        textcoords="offset points",
        fontsize=11,
        fontweight="bold"
    )

# Title and axis labels
ax.set_title(
    "Clinical Trials by Funder Classification",
    fontsize=16,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Funder Type", fontsize=12)
ax.set_ylabel("Percentage of Clinical Trials (%)", fontsize=12)

# Improve gridlines
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

# Remove unnecessary borders
sns.despine()

# Set axis limits and labels
plt.xticks(rotation=0)
plt.ylim(0, max(100, funder_percentages.max() * 1.10))

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/funder_type_distribution.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()



## Analyze the relationship between funding and study enrollment

# Compare enrollment across funding categories
print("\nEnrollment Statistics by Funder Type:")

funding_enrollment = (
    df.groupby("Funder Type")["Enrollment"]
    .agg(["count", "mean", "median", "sum"])
    .sort_values("median", ascending=False)
)

print(funding_enrollment.to_string())

## Analyze enrollment by study start year and funding type

# Calculate median enrollment for each year and funding category
funding_year_enrollment = (
    df.groupby(["Start Year", "Funder Type"])["Enrollment"]
    .agg(["count", "median", "mean"])
    .reset_index()
)

# Display enrollment statistics for selected years
selected_years = [2009, 2010, 2024, 2025, 2026]

print("\nEnrollment by Funding Type for Selected Years:")

print(
    funding_year_enrollment[
        funding_year_enrollment["Start Year"].isin(selected_years)
    ].to_string(index=False)
)

# Compare overall enrollment across selected years
print("\nOverall Enrollment by Study Start Year:")

year_enrollment = (
    df.groupby("Start Year")["Enrollment"]
    .agg(["count", "median", "mean"])
)

print(
    year_enrollment.loc[
        year_enrollment.index.isin(selected_years)
    ].to_string()
)

##visualise

## Analyze enrollment trends by funding type and study start year

# Calculate median enrollment and number of trials
funding_year_summary = (
    df.groupby(["Start Year", "Funder Type"])["Enrollment"]
    .agg(["count", "median"])
    .reset_index()
)

# Include groups with at least five trials
funding_year_filtered = funding_year_summary[
    funding_year_summary["count"] >= 5
]

# Reshape data for visualization
funding_year_pivot = funding_year_filtered.pivot(
    index="Start Year",
    columns="Funder Type",
    values="median"
)

# Set different colours for funding categories
funding_colors = {
    "INDUSTRY": "#2563A6",
    "OTHER": "#16A085",
    "OTHER_GOV": "#7E57C2",
    "NIH": "#66A61E",
    "FED": "#D4A017",
    "NETWORK": "#64748B",
    "INDIV": "#8C6D62"
}

# Create line chart
fig, ax = plt.subplots(figsize=(12, 7))

for funder in funding_year_pivot.columns:
    ax.plot(
        funding_year_pivot.index,
        funding_year_pivot[funder],
        marker="o",
        linewidth=2,
        markersize=5,
        label=funder,
        color=funding_colors.get(funder)
    )

# Title and axis labels
ax.set_title(
    "Median Clinical Trial Enrollment by Funding Type and Start Year",
    fontsize=15,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Study Start Year")
ax.set_ylabel("Median Number of Participants")

# Improve chart formatting
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

sns.despine()

# Display funding categories
ax.legend(title="Funder Type", frameon=False)

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/enrollment_by_funding_and_year.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()

## Heatmap of median enrollment by funding type and study start year

# Calculate median enrollment and number of trials
funding_heatmap_summary = (
    df.groupby(["Start Year", "Funder Type"])["Enrollment"]
    .agg(["count", "median"])
    .reset_index()
)

# Include groups with at least five trials
funding_heatmap_filtered = funding_heatmap_summary[
    funding_heatmap_summary["count"] >= 5
]


# Reshape data for heatmap
funding_heatmap_data = funding_heatmap_filtered.pivot(
    index="Funder Type",
    columns="Start Year",
    values="median"
)

# Display recent study start years
funding_heatmap_data = funding_heatmap_data.loc[
    :, funding_heatmap_data.columns >= 2013
]

# Remove funding categories with no data in the selected years
funding_heatmap_data = funding_heatmap_data.dropna(how="all")

# Focus on the three largest funding categories
funding_heatmap_data = funding_heatmap_data.reindex(
    ["INDUSTRY", "OTHER", "OTHER_GOV"]
)
# Create heatmap
fig, ax = plt.subplots(figsize=(14, 3.8))

# Use a clean white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Plot median enrollment
sns.heatmap(
    funding_heatmap_data,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    linewidths=1.5,
    linecolor="white",
    mask=funding_heatmap_data.isna(),
    annot_kws={"size": 9},
    cbar_kws={
        "label": "Median Participants",
        "shrink": 0.8,
        "pad": 0.02
    },
    ax=ax
)

# Title and axis labels
ax.set_title(
    "Median Clinical Trial Enrollment by Funding Type and Start Year",
    fontsize=15,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Study Start Year", fontsize=11)
ax.set_ylabel("Funder Type", fontsize=11)

# Improve tick labels
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=0,
    fontsize=9
)

ax.set_yticklabels(
    ax.get_yticklabels(),
    rotation=0,
    fontsize=10
)

# Remove background gridlines
ax.grid(False)

# Remove tick marks
ax.tick_params(axis="both", length=0)

plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/enrollment_funding_heatmap.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


## Stacked bar chart of clinical trials by funding type and study start year

# Count trials by start year and funding category
funding_year_counts = (
    df.groupby(["Start Year", "Funder Type"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

# Set different colours for funding categories
funding_colors = {
    "INDUSTRY": "#2563A6",
    "OTHER": "#16A085",
    "OTHER_GOV": "#7E57C2",
    "NIH": "#66A61E",
    "FED": "#D4A017",
    "NETWORK": "#64748B",
    "INDIV": "#8C6D62"
}

# Match colours to funding categories
colors = [
    funding_colors.get(funder, "#999999")
    for funder in funding_year_counts.columns
]

# Create stacked bar chart
fig, ax = plt.subplots(figsize=(13, 7))

funding_year_counts.plot(
    kind="bar",
    stacked=True,
    color=colors,
    edgecolor="white",
    linewidth=0.3,
    width=0.8,
    ax=ax
)

# Title and axis labels
ax.set_title(
    "Clinical Trials by Funding Type and Study Start Year",
    fontsize=16,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Study Start Year", fontsize=12)
ax.set_ylabel("Number of Clinical Trials", fontsize=12)

# Improve gridlines
ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.grid(axis="x", visible=False)
ax.set_axisbelow(True)

# Remove unnecessary borders
sns.despine()

# Display legend
ax.legend(
    title="Funder Type",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=False
)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the figure
plt.savefig(
    "figures/funding_stacked_barplot.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

#plt.show()


##export cleaned  Dataset
# Export cleaned dataset for Power BI
df.to_csv(
    "Data/clinical_trials_cleaned.csv",
    index=False
)

print("\nCleaned dataset exported successfully!")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

##condition

import pandas as pd

# Load the cleaned clinical trial dataset
df = pd.read_csv("Data/clinical_trials_cleaned.csv")

# Keep study IDs and conditions
conditions = df[["NCT Number", "Conditions"]].copy()

# Separate multiple conditions into individual rows
conditions["Conditions"] = conditions["Conditions"].fillna("")
conditions["Conditions"] = conditions["Conditions"].str.split("|")
conditions = conditions.explode("Conditions")

# Clean condition names
conditions["Conditions"] = conditions["Conditions"].str.strip()
conditions = conditions[conditions["Conditions"] != ""]

# Remove duplicate study-condition combinations
conditions = conditions.drop_duplicates()

# Export for Power BI
conditions.to_csv("Data/clinical_trial_conditions.csv", index=False)

print("Total condition records:", len(conditions))
print("Unique conditions:", conditions["Conditions"].nunique())
print(conditions.head())


# Focusing on Drug Trials

## Extract clinical drug trials from the dataset


# Identify studies with drug interventions
if "Intervention Types" not in df.columns:
    raise ValueError(
        "Intervention Types column is missing. "
        "Update the fetch and processing scripts before extracting drug trials."
    )

drug_trials = df[
    df["Intervention Types"]
    .fillna("")
    .str.split("|")
    .apply(lambda types: "DRUG" in [t.strip().upper() for t in types])
].copy()

## Examine how clinical trial interventions are recorded

# Display the first 20 non-missing interventions
print("\nFirst 20 Interventions:")
print(df["Interventions"].dropna().head(20).to_string(index=False))

# Search for examples containing the word drug
print("\nInterventions containing 'DRUG':")
print(
    df.loc[
        df["Interventions"].fillna("").str.contains(
            "DRUG", case=False, regex=False
        ),
        ["NCT Number", "Interventions"]
    ].head(10).to_string(index=False)
)
# Check how interventions are recorded
print("\nExamples of Clinical Trial Interventions:")
print(df["Interventions"].dropna().head(10).to_string(index=False))

# Identify studies with drug interventions
if "Intervention Types" not in df.columns:
    raise ValueError(
        "Intervention Types column is missing. "
        "Update the fetch and processing scripts before extracting drug trials."
    )

drug_trials = df[
    df["Intervention Types"]
    .fillna("")
    .str.split("|")
    .apply(lambda types: "DRUG" in [t.strip().upper() for t in types])
].copy()

# Display the number of drug trials
print("\nTotal Clinical Trials:", len(df))
print("Total Drug Trials:", len(drug_trials))

# Calculate percentage of drug trials
drug_percentage = len(drug_trials) / len(df) * 100

print(f"Percentage of Drug Trials: {drug_percentage:.1f}%")

# Examine funding categories
print("\nDrug Trials by Funder Type:")
print(drug_trials["Funder Type"].value_counts())

# Examine study phases
print("\nDrug Trials by Study Phase:")
print(drug_trials["Phases"].value_counts(dropna=False))

# Examine enrollment
print("\nDrug Trial Enrollment Statistics:")
print(drug_trials["Enrollment"].describe())


# Compare drug trials across funding categories
df["Is Drug Trial"] = df["Intervention Types"].fillna("").str.split("|").apply(
    lambda types: "DRUG" in [t.strip().upper() for t in types]
)

funding_comparison = pd.crosstab(
    df["Funder Type"],
    df["Is Drug Trial"]
)

funding_comparison.columns = ["Non-Drug Trials", "Drug Trials"]

funding_comparison["Drug Trial Percentage"] = (
    funding_comparison["Drug Trials"]
    / funding_comparison.sum(axis=1) * 100
).round(1)

print("\nDrug Trial Distribution by Funding Category:")
print(funding_comparison)

##visualise
# Visualize drug and non-drug trial percentages by funder
funding_percentages = funding_comparison[
    ["Non-Drug Trials", "Drug Trials"]
].div(
    funding_comparison[
        ["Non-Drug Trials", "Drug Trials"]
    ].sum(axis=1),
    axis=0
) * 100

# Exclude INDIV because it contains only one trial
funding_percentages = funding_percentages.drop(
    index="INDIV",
    errors="ignore"
)

funding_percentages = funding_percentages.sort_values(
    "Drug Trials",
    ascending=False
)

ax = funding_percentages.plot(
    kind="barh",
    stacked=True,
    figsize=(10, 6),
    color=["#B0BEC5", "#1976D2"]
)

ax.set_title("Drug vs Non-Drug Trials by Funding Category")
ax.set_xlabel("Percentage of Trials (%)")
ax.set_ylabel("Funding Category")
ax.set_xlim(0, 100)
ax.legend(
    title="Trial Classification",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=2,
    frameon=False
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)
plt.show()


# ============================================================
# Distribution of All Clinical Trial Intervention Types
# ============================================================

# Separate multiple intervention types
intervention_types = (
    df["Intervention Types"]
    .dropna()
    .str.split("|")
    .explode()
    .str.strip()
    .str.upper()
)

# Remove empty values
intervention_types = intervention_types[
    intervention_types != ""
]

# Count each intervention type
intervention_counts = intervention_types.value_counts()

# Create horizontal bar chart
plt.figure(figsize=(11, 7))

ax = intervention_counts.sort_values().plot(
    kind="barh",
    color="steelblue"
)

# Add count labels
for i, value in enumerate(intervention_counts.sort_values()):
    ax.text(
        value + 5,
        i,
        str(value),
        va="center"
    )

plt.title("Distribution of Intervention Types in Clinical Trials")
plt.xlabel("Number of Interventions")
plt.ylabel("Intervention Type")

plt.xlim(0, intervention_counts.max() * 1.15)

plt.tight_layout()
plt.show()

# Display intervention counts
print("\nDistribution of Intervention Types:")
print(intervention_counts)



import matplotlib.pyplot as plt

labels = ["Drug trials", "Non-drug trials"]
values = [1556, 3444]
colors = ["#1765A3", "#DCE8F3"]

fig, ax = plt.subplots(figsize=(7, 5))

ax.pie(
    values,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops={"width": 0.35, "edgecolor": "white"}
)

ax.text(0, 0.08, "5,000", ha="center",
        va="center", fontsize=24, fontweight="bold")
ax.text(0, -0.17, "Total trials", ha="center",
        fontsize=12)

ax.legend(
    [f"{label}: {value:,} ({value / sum(values):.1%})"
     for label, value in zip(labels, values)],
    loc="lower center",
    bbox_to_anchor=(0.5, -0.15),
    frameon=False,
    ncol=2
)

ax.set_title("Drug vs. Non-Drug Clinical Trials",
             fontsize=15, fontweight="bold")

plt.savefig("drug_vs_non_drug_donut.png",
            dpi=300, bbox_inches="tight")
plt.show()
