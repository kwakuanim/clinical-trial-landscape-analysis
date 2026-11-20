
import ast
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

INPUT_FILE = DATA_DIR / "clinical_trials_full_5000.csv"

TRIALS_OUTPUT = DATA_DIR / "clinical_trials_cleaned_5000.csv"
CONDITIONS_OUTPUT = DATA_DIR / "clinical_trial_conditions_5000.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input dataset not found: {INPUT_FILE}"
    )

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(
    INPUT_FILE,
    dtype={"NCT Number": "string"}
)

print("Original records:", len(df))

# --------------------------------------------------
# 3. Validate study identifiers
# --------------------------------------------------

assert len(df) == 5000, (
    f"Expected 5000 trials, found {len(df)}"
)

assert df["NCT Number"].notna().all(), (
    "Missing NCT numbers detected"
)

assert df["NCT Number"].is_unique, (
    "Duplicate NCT numbers detected"
)

# --------------------------------------------------
# 4. Verify study selection
# --------------------------------------------------

assert df["Study Status"].eq("COMPLETED").all(), (
    "Dataset contains studies that are not COMPLETED"
)

assert df["Study Type"].eq("INTERVENTIONAL").all(), (
    "Dataset contains non-interventional studies"
)

# --------------------------------------------------
# 5. Convert dates
# --------------------------------------------------

date_columns = [
    "Start Date",
    "Primary Completion Date",
    "Completion Date"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        format="mixed",
        errors="coerce"
    )

# --------------------------------------------------
# 6. Generate Start Year
# --------------------------------------------------

df["Start Year"] = (
    df["Start Date"]
    .dt.year
    .astype("Int64")
)

# --------------------------------------------------
# 7. Convert enrollment to numeric
# --------------------------------------------------

df["Enrollment"] = pd.to_numeric(
    df["Enrollment"],
    errors="coerce"
)

if df["Enrollment"].lt(0).any():
    raise ValueError(
        "Negative enrollment values detected"
    )

# --------------------------------------------------
# 8. Standardize missing phases
# --------------------------------------------------

df["Phases"] = df["Phases"].replace(
    r"^\s*$",
    pd.NA,
    regex=True
)

# --------------------------------------------------
# 9. Clean age information
# --------------------------------------------------

def clean_age(value):
    if pd.isna(value):
        return ""

    try:
        parsed = ast.literal_eval(str(value))

        if isinstance(parsed, list):
            return "|".join(
                str(item) for item in parsed
            )

    except (ValueError, SyntaxError):
        pass

    return str(value)


df["Age"] = df["Age"].apply(clean_age)

# --------------------------------------------------
# 10. Create conditions table
# --------------------------------------------------

conditions_df = df[
    ["NCT Number", "Conditions"]
].copy()

conditions_df["Conditions"] = (
    conditions_df["Conditions"]
    .fillna("")
    .str.split("|", regex=False)
)

conditions_df = conditions_df.explode(
    "Conditions"
)

conditions_df["Conditions"] = (
    conditions_df["Conditions"]
    .fillna("")
    .str.strip()
)

conditions_df = conditions_df[
    conditions_df["Conditions"] != ""
].copy()

conditions_df = conditions_df.drop_duplicates(
    subset=["NCT Number", "Conditions"]
)

# --------------------------------------------------
# 11. Save processed datasets
# --------------------------------------------------

df.to_csv(
    TRIALS_OUTPUT,
    index=False,
    encoding="utf-8-sig",
    date_format="%Y-%m-%d"
)

conditions_df.to_csv(
    CONDITIONS_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# 12. Validation summary
# --------------------------------------------------

print("\n=== PROCESSING COMPLETE ===")

print("Total trials:", len(df))
print("Unique trials:", df["NCT Number"].nunique())

print("Missing phases:", df["Phases"].isna().sum())
print("Missing start years:", df["Start Year"].isna().sum())

print("Condition records:", len(conditions_df))
print("Unique conditions:", conditions_df["Conditions"].nunique())

print("Total enrollment:", df["Enrollment"].sum())
print("Median enrollment:", df["Enrollment"].median())

print("\nFiles created:")
print(TRIALS_OUTPUT)
print(CONDITIONS_OUTPUT)
