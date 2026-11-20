
"""
Clinical Trial Landscape Analysis
Raw Dataset Validation

Validates the ClinicalTrials.gov dataset before processing.

Input:
    Data/clinical_trials_full_5000.csv

Author: Manfred Anim
"""

from pathlib import Path

import pandas as pd


# ============================================================
# 1. FILE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "Data"
    / "clinical_trials_full_5000.csv"
)

if not DATA_FILE.is_file():
    raise FileNotFoundError(
        f"Raw dataset not found: {DATA_FILE}\n"
        "Run fetch.py first."
    )


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(
    DATA_FILE,
    dtype={"NCT Number": "string"}
)

print("\n=== CLINICAL TRIAL DATA VALIDATION ===")

print("\n=== DATASET OVERVIEW ===")
print("Total trials:", len(df))
print("Unique NCT numbers:", df["NCT Number"].nunique())
print("Number of columns:", len(df.columns))


# ============================================================
# 3. REQUIRED COLUMNS
# ============================================================

required_columns = [
    "NCT Number",
    "Study Title",
    "Study Status",
    "Study Type",
    "Conditions",
    "Interventions",
    "Intervention Types",
    "Enrollment",
    "Enrollment Type",
    "Phases",
    "Funder Type",
    "Start Date"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("\nRequired columns: PASS")


# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n=== MISSING VALUES ===")

missing_values = df.isna().sum()

print(missing_values.to_string())


# ============================================================
# 5. DATA TYPES
# ============================================================

print("\n=== DATA TYPES ===")

print(df.dtypes.to_string())


# ============================================================
# 6. NCT IDENTIFIER VALIDATION
# ============================================================

duplicates = int(
    df["NCT Number"].duplicated().sum()
)

missing_ids = int(
    df["NCT Number"].isna().sum()
)

invalid_id_format = int(
    (
        ~df["NCT Number"]
        .fillna("")
        .str.fullmatch(r"NCT\d{8}")
    ).sum()
)

print("\n=== NCT IDENTIFIERS ===")

print("Duplicate NCT numbers:", duplicates)
print("Missing NCT numbers:", missing_ids)
print("Invalid NCT ID formats:", invalid_id_format)


# ============================================================
# 7. STUDY STATUS AND TYPE
# ============================================================

print("\n=== STUDY STATUS ===")

print(
    df["Study Status"]
    .value_counts(dropna=False)
    .to_string()
)

print("\n=== STUDY TYPE ===")

print(
    df["Study Type"]
    .value_counts(dropna=False)
    .to_string()
)

invalid_status = int(
    (
        df["Study Status"]
        .fillna("")
        .ne("COMPLETED")
    ).sum()
)

invalid_type = int(
    (
        df["Study Type"]
        .fillna("")
        .ne("INTERVENTIONAL")
    ).sum()
)

print("\nInvalid study statuses:", invalid_status)
print("Invalid study types:", invalid_type)


# ============================================================
# 8. ENROLLMENT VALIDATION
# ============================================================

original_enrollment = df["Enrollment"].copy()

df["Enrollment"] = pd.to_numeric(
    df["Enrollment"],
    errors="coerce"
)

missing_enrollment = int(
    df["Enrollment"].isna().sum()
)

negative_enrollment = int(
    df["Enrollment"].lt(0).sum()
)

invalid_enrollment = int(
    (
        original_enrollment.notna()
        & df["Enrollment"].isna()
    ).sum()
)

print("\n=== ENROLLMENT SUMMARY ===")

print(df["Enrollment"].describe())

print("Missing enrollment:", missing_enrollment)
print("Negative enrollment:", negative_enrollment)
print("Invalid numeric values:", invalid_enrollment)


# ============================================================
# 9. ENROLLMENT TYPE
# ============================================================

print("\n=== ENROLLMENT TYPE ===")

print(
    df["Enrollment Type"]
    .value_counts(dropna=False)
    .to_string()
)


# ============================================================
# 10. INTERVENTION TYPES
# ============================================================

print("\n=== INTERVENTION TYPES ===")

missing_intervention_types = int(
    (
        df["Intervention Types"]
        .isna()
        | df["Intervention Types"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    ).sum()
)

print(
    "Missing intervention types:",
    missing_intervention_types
)

intervention_counts = (
    df["Intervention Types"]
    .dropna()
    .str.split("|", regex=False)
    .explode()
    .str.strip()
    .str.upper()
    .value_counts()
)

print("\nIntervention type counts:")
print(intervention_counts.to_string())


# ============================================================
# 11. TOP FIVE LARGEST TRIALS
# ============================================================

print("\n=== TOP 5 TRIALS BY ENROLLMENT ===")

top_trials = df.nlargest(
    5,
    "Enrollment"
)[
    [
        "NCT Number",
        "Study Title",
        "Enrollment"
    ]
]

print(
    top_trials.to_string(index=False)
)


# ============================================================
# 12. FINAL VALIDATION
# ============================================================

checks = {
    "Expected 5,000 trials": len(df) == 5000,

    "Unique NCT numbers": duplicates == 0,

    "No missing NCT numbers": missing_ids == 0,

    "Valid NCT identifier formats": invalid_id_format == 0,

    "Completed studies only": invalid_status == 0,

    "Interventional studies only": invalid_type == 0,

    "No negative enrollment": negative_enrollment == 0,

    "No invalid enrollment values": invalid_enrollment == 0
}

print("\n=== VALIDATION SUMMARY ===")

for name, passed in checks.items():
    status = "PASS" if passed else "FAIL"

    print(f"{name}: {status}")

if not all(checks.values()):
    raise ValueError(
        "Validation failed. Review the checks above."
    )

print("\nVALIDATION SUCCESSFUL")

print("\n=== FINAL DATASET SUMMARY ===")

print("Total trials:", len(df))

print(
    "Unique NCT numbers:",
    df["NCT Number"].nunique()
)

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
    "Missing intervention types:",
    missing_intervention_types
)

print("\nDataset is ready for processing.")
