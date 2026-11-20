
import pandas as pd
from pathlib import Path

# File locations
DATA_DIR = Path("Data")
INPUT_FILE = DATA_DIR / "clinical_trials_full_5000.csv"

TRIALS_OUTPUT = DATA_DIR / "clinical_trials_cleaned_5000.csv"
CONDITIONS_OUTPUT = DATA_DIR / "clinical_trial_conditions_5000.csv"

# 1. Load the downloaded dataset
df = pd.read_csv(INPUT_FILE, dtype={"NCT Number": "string"})

print("Original records:", len(df))

# 2. Check study identifiers
assert df["NCT Number"].notna().all(), "Missing NCT numbers"
assert df["NCT Number"].is_unique, "Duplicate NCT numbers"

# 3. Verify study selection
assert df["Study Status"].eq("COMPLETED").all()
assert df["Study Type"].eq("INTERVENTIONAL").all()

# 4. Convert dates
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

# 5. Generate Start Year
df["Start Year"] = df["Start Date"].dt.year.astype("Int64")

# 6. Convert enrollment to numeric
df["Enrollment"] = pd.to_numeric(
    df["Enrollment"],
    errors="coerce"
)

# 7. Standardize missing phases
df["Phases"] = df["Phases"].replace(
    r"^\s*$", pd.NA, regex=True
)

# 8. Prepare the Age column
# Convert string representations of lists into readable values
import ast

def clean_age(value):
    if pd.isna(value):
        return ""

    try:
        parsed = ast.literal_eval(str(value))
        if isinstance(parsed, list):
            return "|".join(str(item) for item in parsed)
    except (ValueError, SyntaxError):
        pass

    return str(value)

df["Age"] = df["Age"].apply(clean_age)

# 9. Create the conditions table
conditions_df = df[
    ["NCT Number", "Conditions"]
].copy()

conditions_df["Conditions"] = conditions_df[
    "Conditions"
].fillna("").str.split("|", regex=False)

conditions_df = conditions_df.explode("Conditions")

conditions_df["Conditions"] = (
    conditions_df["Conditions"]
    .fillna("")
    .str.strip()
)

conditions_df = conditions_df[
    conditions_df["Conditions"] != ""
]

conditions_df = conditions_df.drop_duplicates(
    subset=["NCT Number", "Conditions"]
)

# 10. Save the datasets
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

# 11. Validation summary
print("\n=== PROCESSING COMPLETE ===")
print("Total trials:", len(df))
print("Unique trials:", df["NCT Number"].nunique())
print("Missing phases:", df["Phases"].isna().sum())
print("Missing start years:", df["Start Year"].isna().sum())
print("Condition records:", len(conditions_df))
print("Unique conditions:", conditions_df["Conditions"].nunique())
print("Median enrollment:", df["Enrollment"].median())

print("\nFiles created:")
print(TRIALS_OUTPUT)
print(CONDITIONS_OUTPUT)
