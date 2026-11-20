
"""
Clinical Trial Landscape Analysis
Exploratory Data Analysis and Visualization

Data source: ClinicalTrials.gov
Dataset: 5,000 completed interventional studies

Input:
    Data/clinical_trials_cleaned_5000.csv
    Data/clinical_trial_conditions_5000.csv

Output:
    Nine figures saved in figures/

Author: Manfred Anim
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "Data"
FIGURES_DIR = BASE_DIR / "figures"

TRIALS_FILE = DATA_DIR / "clinical_trials_cleaned_5000.csv"
CONDITIONS_FILE = DATA_DIR / "clinical_trial_conditions_5000.csv"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(
    style="whitegrid",
    context="notebook",
    font_scale=1.1
)

plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# Consistent funding colors
FUNDING_COLORS = {
    "INDUSTRY": "#2563A6",
    "OTHER": "#16A085",
    "OTHER_GOV": "#7E57C2",
    "NIH": "#66A61E",
    "FED": "#D4A017",
    "NETWORK": "#64748B",
    "INDIV": "#8C6D62"
}


def save_figure(fig, filename):
    """Save a figure and close it."""

    output_path = FIGURES_DIR / filename

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)

    print(f"Figure saved: {output_path.name}")


def format_chart(ax, grid_axis="y"):
    """Apply consistent chart formatting."""

    ax.set_axisbelow(True)

    ax.grid(
        axis=grid_axis,
        linestyle="--",
        alpha=0.25
    )

    other_axis = "x" if grid_axis == "y" else "y"
    ax.grid(axis=other_axis, visible=False)

    sns.despine(ax=ax)


# ============================================================
# 2. LOAD AND VALIDATE DATA
# ============================================================

print("\n=== LOADING CLINICAL TRIAL DATA ===")

if not TRIALS_FILE.exists():
    raise FileNotFoundError(
        f"Missing dataset: {TRIALS_FILE}\n"
        "Run process_clinical_trials.py first."
    )

if not CONDITIONS_FILE.exists():
    raise FileNotFoundError(
        f"Missing conditions dataset: {CONDITIONS_FILE}\n"
        "Run process_clinical_trials.py first."
    )

df = pd.read_csv(
    TRIALS_FILE,
    dtype={"NCT Number": "string"}
)

conditions_df = pd.read_csv(
    CONDITIONS_FILE,
    dtype={"NCT Number": "string"}
)

required_columns = [
    "NCT Number",
    "Study Title",
    "Study Status",
    "Study Type",
    "Start Year",
    "Enrollment",
    "Phases",
    "Funder Type",
    "Intervention Types"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

if not {"NCT Number", "Conditions"}.issubset(
    conditions_df.columns
):
    raise ValueError(
        "Conditions dataset must contain "
        "'NCT Number' and 'Conditions'."
    )

if df["NCT Number"].isna().any():
    raise ValueError("Missing NCT identifiers detected.")

if df["NCT Number"].duplicated().any():
    raise ValueError("Duplicate NCT identifiers detected.")

if not df["Study Status"].eq("COMPLETED").all():
    raise ValueError(
        "Dataset contains studies that are not completed."
    )

if not df["Study Type"].eq("INTERVENTIONAL").all():
    raise ValueError(
        "Dataset contains non-interventional studies."
    )

df["Enrollment"] = pd.to_numeric(
    df["Enrollment"],
    errors="coerce"
)

df["Start Year"] = pd.to_numeric(
    df["Start Year"],
    errors="coerce"
).astype("Int64")

df["Phases"] = df["Phases"].replace(
    r"^\s*$",
    pd.NA,
    regex=True
)

df["Funder Type"] = df["Funder Type"].replace(
    r"^\s*$",
    pd.NA,
    regex=True
)

if df["Enrollment"].lt(0).any():
    raise ValueError("Negative enrollment detected.")

# Check conditions-table integrity
if conditions_df["NCT Number"].isna().any():
    raise ValueError(
        "Conditions table contains missing NCT identifiers."
    )

unknown_ids = (
    set(conditions_df["NCT Number"].dropna())
    - set(df["NCT Number"])
)

if unknown_ids:
    raise ValueError(
        f"Conditions table contains {len(unknown_ids)} "
        "unknown NCT identifiers."
    )

conditions_df["Conditions"] = (
    conditions_df["Conditions"]
    .fillna("")
    .astype(str)
    .str.strip()
)

conditions_df = conditions_df[
    conditions_df["Conditions"] != ""
].copy()

conditions_df = conditions_df.drop_duplicates(
    subset=["NCT Number", "Conditions"]
)

print("Total trials:", len(df))
print("Unique NCT IDs:", df["NCT Number"].nunique())
print("Dataset columns:", len(df.columns))
print("Missing phases:", df["Phases"].isna().sum())
print("Missing start years:", df["Start Year"].isna().sum())
print("Missing enrollment:", df["Enrollment"].isna().sum())

print(
    "Total reported enrollment:",
    f"{df['Enrollment'].sum():,.0f}"
)

print(
    "Median enrollment:",
    df["Enrollment"].median()
)

print("Condition records:", len(conditions_df))
print("Unique conditions:", conditions_df["Conditions"].nunique())

if len(df) != 5000:
    print(
        "WARNING: The dataset does not contain exactly "
        "5,000 trials."
    )


# ============================================================
# 3. DRUG VS NON-DRUG CLASSIFICATION
# ============================================================

print("\n=== DRUG VS NON-DRUG CLASSIFICATION ===")

def contains_drug(intervention_types):
    """Identify studies reporting a DRUG intervention."""

    if pd.isna(intervention_types):
        return False

    types = [
        item.strip().upper()
        for item in str(intervention_types).split("|")
    ]

    return "DRUG" in types


df["Is Drug Trial"] = (
    df["Intervention Types"].apply(contains_drug)
)

missing_intervention_types = (
    df["Intervention Types"]
    .isna()
    .sum()
)

drug_count = int(df["Is Drug Trial"].sum())
non_drug_count = int((~df["Is Drug Trial"]).sum())

total_trials = len(df)

print("Drug trials:", drug_count)
print("Non-drug trials:", non_drug_count)
print("Total trials:", total_trials)

print(
    "Drug trial percentage:",
    f"{drug_count / total_trials * 100:.1f}%"
)

print(
    "Non-drug trial percentage:",
    f"{non_drug_count / total_trials * 100:.1f}%"
)

print(
    "Missing intervention types:",
    missing_intervention_types
)

if missing_intervention_types > 0:
    print(
        "WARNING: Studies with missing intervention types "
        "are classified as non-drug under the current rule."
    )


# ============================================================
# FIGURE 1: DRUG VS NON-DRUG CLINICAL TRIALS
# ============================================================

print("\n=== FIGURE 1: DRUG VS NON-DRUG ===")

labels = [
    "Drug trials",
    "Non-drug trials"
]

values = [
    drug_count,
    non_drug_count
]

colors = [
    "#1765A3",
    "#DCE8F3"
]

fig, ax = plt.subplots(figsize=(8, 7))

ax.pie(
    values,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops={
        "width": 0.35,
        "edgecolor": "white"
    }
)

ax.text(
    0, 0.08,
    f"{total_trials:,}",
    ha="center",
    va="center",
    fontsize=23,
    fontweight="bold"
)

ax.text(
    0, -0.15,
    "Total trials",
    ha="center",
    va="center",
    fontsize=11
)

legend_labels = [
    f"{label}: {value:,} ({value / total_trials:.1%})"
    for label, value in zip(labels, values)
]

ax.legend(
    legend_labels,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.05),
    fontsize=11,
    frameon=False,
    ncol=1,
    labelspacing=0.9
)

ax.set_title(
    "Drug vs. Non-Drug Clinical Trials",
    pad=20
)

fig.tight_layout()

save_figure(
    fig,
    "Drug vs non drug.png"
)


# ============================================================
# FIGURE 2: CLINICAL TRIALS BY START YEAR
# ============================================================

print("\n=== FIGURE 2: CLINICAL TRIALS BY YEAR ===")

trials_per_year = (
    df["Start Year"]
    .dropna()
    .value_counts()
    .sort_index()
)

print(trials_per_year.to_string())

fig, ax = plt.subplots(figsize=(11, 6.5))

ax.plot(
    trials_per_year.index.to_numpy(dtype=int),
    trials_per_year.values,
    marker="o",
    color="#7B2CBF",
    linewidth=2.5,
    markersize=7,
    markerfacecolor="white",
    markeredgewidth=2
)

ax.set_title("Clinical Trials by Start Year", pad=20)
ax.set_xlabel("Study Start Year")
ax.set_ylabel("Number of Clinical Trials")

ax.set_xticks(
    trials_per_year.index.to_numpy(dtype=int)
)

ax.tick_params(axis="x", rotation=45)
ax.set_ylim(bottom=0)

format_chart(ax, grid_axis="y")

fig.tight_layout()

save_figure(
    fig,
    "Clinical trials by year.png"
)


# ============================================================
# FIGURE 3: MEDIAN ENROLLMENT BY START YEAR
# ============================================================

print("\n=== FIGURE 3: MEDIAN ENROLLMENT BY YEAR ===")

median_enrollment_by_year = (
    df.groupby("Start Year")["Enrollment"]
    .median()
    .dropna()
    .sort_index()
)

print(median_enrollment_by_year.to_string())

fig, ax = plt.subplots(figsize=(11, 6.5))

ax.plot(
    median_enrollment_by_year.index.to_numpy(dtype=int),
    median_enrollment_by_year.values,
    marker="o",
    color="#D97706",
    linewidth=2.5,
    markersize=7,
    markerfacecolor="white",
    markeredgewidth=2
)

ax.set_title(
    "Median Clinical Trial Enrollment by Start Year",
    pad=20
)

ax.set_xlabel("Study Start Year")
ax.set_ylabel("Median Number of Participants")

ax.set_xticks(
    median_enrollment_by_year.index.to_numpy(dtype=int)
)

ax.tick_params(axis="x", rotation=45)
ax.set_ylim(bottom=0)

for year, median in median_enrollment_by_year.items():
    ax.annotate(
        f"{median:,.0f}",
        (int(year), median),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold",
        color="#92400E"
    )

format_chart(ax, grid_axis="y")

fig.tight_layout()

save_figure(
    fig,
    "Median enrollment.png"
)


# ============================================================
# FIGURE 4: ENROLLMENT DISTRIBUTION
# ============================================================

print("\n=== FIGURE 4: ENROLLMENT DISTRIBUTION ===")

print(df["Enrollment"].describe())

enrollment_positive = (
    df["Enrollment"]
    .dropna()
)

enrollment_positive = enrollment_positive[
    enrollment_positive > 0
]

if enrollment_positive.empty:
    raise ValueError(
        "No positive enrollment values available."
    )

min_enrollment = enrollment_positive.min()
max_enrollment = enrollment_positive.max()

if min_enrollment == max_enrollment:
    bins = np.array([
        min_enrollment * 0.9,
        max_enrollment * 1.1
    ])
else:
    bins = np.logspace(
        np.log10(min_enrollment),
        np.log10(max_enrollment),
        30
    )

fig, ax = plt.subplots(figsize=(11, 6.5))

ax.hist(
    enrollment_positive,
    bins=bins,
    color="#34699A",
    edgecolor="white",
    linewidth=0.8,
    alpha=0.9
)

ax.set_xscale("log")

ax.set_title(
    "Distribution of Clinical Trial Enrollment",
    pad=20
)

ax.set_xlabel("Number of Participants (Log Scale)")
ax.set_ylabel("Number of Clinical Trials")

format_chart(ax, grid_axis="y")

fig.tight_layout()

save_figure(
    fig,
    "Enrollment_distribution.png"
)

print(
    "Studies excluded from log plot "
    "(zero or missing enrollment):",
    len(df) - len(enrollment_positive)
)

print("\nTop 10 Clinical Trials by Enrollment:")

top_enrollment = df.nlargest(
    10,
    "Enrollment"
)

print(
    top_enrollment[
        ["NCT Number", "Study Title", "Enrollment", "Phases"]
    ].to_string(index=False)
)


# ============================================================
# FIGURE 5: STUDY PHASE DISTRIBUTION
# ============================================================

print("\n=== FIGURE 5: STUDY PHASES ===")

phase_counts = (
    df["Phases"]
    .fillna("Not Reported")
    .value_counts()
    .sort_values(ascending=True)
)

print(
    phase_counts.sort_values(ascending=False).to_string()
)

fig, ax = plt.subplots(figsize=(11, 6.5))

colors = sns.color_palette(
    "viridis",
    n_colors=len(phase_counts)
)

bars = ax.barh(
    phase_counts.index,
    phase_counts.values,
    color=colors,
    height=0.7
)

for bar in bars:
    width = bar.get_width()

    ax.text(
        width + phase_counts.max() * 0.012,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

ax.set_title(
    "Distribution of Clinical Trials by Study Phase",
    pad=20
)

ax.set_xlabel("Number of Clinical Trials")
ax.set_ylabel("Study Phase")

ax.set_xlim(
    0,
    phase_counts.max() * 1.15
)

format_chart(ax, grid_axis="x")

fig.tight_layout()

save_figure(
    fig,
    "Study phases.png"
)


# ============================================================
# FIGURE 6: FUNDING CLASSIFICATION
# ============================================================

print("\n=== FIGURE 6: FUNDING CLASSIFICATION ===")

funder_counts = (
    df["Funder Type"]
    .fillna("Not Reported")
    .value_counts()
)

print(funder_counts.to_string())

funder_percentages = (
    funder_counts / len(df) * 100
)

colors = [
    FUNDING_COLORS.get(category, "#999999")
    for category in funder_percentages.index
]

fig, ax = plt.subplots(figsize=(11, 6.5))

bars = ax.bar(
    funder_percentages.index,
    funder_percentages.values,
    color=colors,
    edgecolor="white",
    width=0.65
)

for bar in bars:
    height = bar.get_height()

    ax.annotate(
        f"{height:.1f}%",
        (
            bar.get_x() + bar.get_width() / 2,
            height
        ),
        ha="center",
        va="bottom",
        xytext=(0, 5),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold"
    )

ax.set_title(
    "Clinical Trials by Funder Classification",
    pad=20
)

ax.set_xlabel("Funder Type")
ax.set_ylabel("Percentage of Clinical Trials (%)")

ax.set_ylim(
    0,
    max(100, funder_percentages.max() * 1.1)
)

ax.tick_params(axis="x", rotation=30)

format_chart(ax, grid_axis="y")

fig.tight_layout()

save_figure(
    fig,
    "Funding classification.png"
)


# ============================================================
# FIGURE 7: DRUG VS NON-DRUG BY FUNDING CATEGORY
# ============================================================

print("\n=== FIGURE 7: DRUG TRIALS BY FUNDING ===")

funding_comparison = pd.crosstab(
    df["Funder Type"].fillna("Not Reported"),
    df["Is Drug Trial"]
)

funding_comparison = funding_comparison.reindex(
    columns=[False, True],
    fill_value=0
)

funding_comparison.columns = [
    "Non-Drug Trials",
    "Drug Trials"
]

funding_comparison["Drug Trial Percentage"] = (
    funding_comparison["Drug Trials"]
    / funding_comparison[
        ["Non-Drug Trials", "Drug Trials"]
    ].sum(axis=1)
    * 100
).round(1)

print(funding_comparison.to_string())

funding_percentages = (
    funding_comparison[
        ["Non-Drug Trials", "Drug Trials"]
    ]
    .div(
        funding_comparison[
            ["Non-Drug Trials", "Drug Trials"]
        ].sum(axis=1),
        axis=0
    )
    * 100
)

# Preserve the original exclusion of INDIV
# because it contains only one trial.
funding_percentages = funding_percentages.drop(
    index="INDIV",
    errors="ignore"
)

funding_percentages = funding_percentages.sort_values(
    "Drug Trials",
    ascending=True
)

fig, ax = plt.subplots(figsize=(11, 6.5))

funding_percentages.plot(
    kind="barh",
    stacked=True,
    ax=ax,
    color=["#B0BEC5", "#1976D2"],
    edgecolor="white"
)

ax.set_title(
    "Drug vs. Non-Drug Trials by Funding Category",
    pad=20
)

ax.set_xlabel("Percentage of Trials (%)")
ax.set_ylabel("Funding Category")
ax.set_xlim(0, 100)

ax.legend(
    title="Trial Classification",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.14),
    ncol=2,
    frameon=False
)

format_chart(ax, grid_axis="x")

fig.tight_layout()

save_figure(
    fig,
    "Drug trials by funding category.png"
)


# ============================================================
# FIGURE 8: FUNDING CATEGORIES BY STUDY START YEAR
# ============================================================

print("\n=== FIGURE 8: FUNDING OVER TIME ===")

funding_year_counts = (
    df.dropna(subset=["Start Year"])
    .assign(
        **{
            "Funder Type": lambda data:
                data["Funder Type"].fillna("Not Reported")
        }
    )
    .groupby(["Start Year", "Funder Type"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

print(funding_year_counts.to_string())

colors = [
    FUNDING_COLORS.get(funder, "#999999")
    for funder in funding_year_counts.columns
]

fig, ax = plt.subplots(figsize=(13, 7))

funding_year_counts.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    color=colors,
    edgecolor="white",
    linewidth=0.3,
    width=0.8
)

ax.set_title(
    "Clinical Trials by Funding Type and Study Start Year",
    pad=20
)

ax.set_xlabel("Study Start Year")
ax.set_ylabel("Number of Clinical Trials")

ax.tick_params(axis="x", rotation=45)

ax.legend(
    title="Funder Type",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=False
)

format_chart(ax, grid_axis="y")

fig.tight_layout()

save_figure(
    fig,
    "Funding over time.png"
)


# ============================================================
# FIGURE 9: TOP 10 MEDICAL CONDITIONS
# ============================================================

print("\n=== FIGURE 9: TOP 10 CONDITIONS ===")

top_conditions = (
    conditions_df["Conditions"]
    .value_counts()
    .head(10)
)

print(top_conditions.to_string())

fig, ax = plt.subplots(figsize=(11, 6.5))

sorted_conditions = top_conditions.sort_values()

colors = sns.color_palette(
    "crest",
    n_colors=len(sorted_conditions)
)

bars = ax.barh(
    sorted_conditions.index,
    sorted_conditions.values,
    color=colors,
    edgecolor="white"
)

for bar in bars:
    width = bar.get_width()

    ax.annotate(
        f"{int(width):,}",
        (
            width,
            bar.get_y() + bar.get_height() / 2
        ),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

ax.set_title(
    "Top 10 Conditions in Completed Clinical Trials",
    pad=20
)

ax.set_xlabel("Number of Clinical Trials")
ax.set_ylabel("Medical Condition")

ax.set_xlim(
    0,
    top_conditions.max() * 1.15
)

format_chart(ax, grid_axis="x")

fig.tight_layout()

save_figure(
    fig,
    "Most frequent condition in completed trials.png"
)


# ============================================================
# 4. ADDITIONAL DESCRIPTIVE ANALYSIS
# ============================================================

print("\n=== ADDITIONAL ENROLLMENT ANALYSIS ===")

funding_enrollment = (
    df.groupby("Funder Type")["Enrollment"]
    .agg(["count", "mean", "median", "sum"])
    .sort_values("median", ascending=False)
)

print("\nEnrollment by Funding Category:")
print(funding_enrollment.to_string())

year_enrollment = (
    df.groupby("Start Year")["Enrollment"]
    .agg(["count", "median", "mean"])
)

print("\nEnrollment by Study Start Year:")
print(year_enrollment.to_string())

print("\nDrug Trial Enrollment Statistics:")

print(
    df.loc[
        df["Is Drug Trial"],
        "Enrollment"
    ].describe()
)

print("\nDrug Trials by Study Phase:")

print(
    df.loc[
        df["Is Drug Trial"],
        "Phases"
    ].value_counts(dropna=False)
)


# ============================================================
# 5. FINAL VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CLINICAL TRIAL LANDSCAPE ANALYSIS COMPLETE")
print("=" * 60)

print(f"Total clinical trials: {len(df):,}")
print(f"Unique NCT IDs: {df['NCT Number'].nunique():,}")

print(f"Drug trials: {drug_count:,}")
print(f"Non-drug trials: {non_drug_count:,}")

print(
    "Total reported enrollment:",
    f"{df['Enrollment'].sum():,.0f}"
)

print(
    "Median enrollment:",
    df["Enrollment"].median()
)

print(
    "Missing phases:",
    df["Phases"].isna().sum()
)

print(
    "Missing start years:",
    df["Start Year"].isna().sum()
)

print(
    "Unique medical conditions:",
    conditions_df["Conditions"].nunique()
)

print("\nFigures generated: 9")
print("Output directory:", FIGURES_DIR)

print("\n=== CHECK AGAINST PREVIOUS RESULTS ===")

expected_results = {
    "Total trials": (len(df), 5000),
    "Drug trials": (drug_count, 1530),
    "Non-drug trials": (non_drug_count, 3470),
    "Total enrollment": (
        int(df["Enrollment"].sum()),
        2425863
    ),
    "Median enrollment": (
        float(df["Enrollment"].median()),
        62.0
    ),
    "Missing phases": (
        int(df["Phases"].isna().sum()),
        3424
    )
}

for metric, (actual, expected) in expected_results.items():
    status = "PASS" if actual == expected else "DIFFERENT"

    print(
        f"{metric}: {actual:,} "
        f"(previously {expected:,}) [{status}]"
    )

print(
    "\nNote: Differences may indicate that the "
    "input dataset has changed. Review them "
    "before updating the README or dashboard."
)

print("\nAnalysis finished successfully.")
