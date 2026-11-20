
import pandas as pd

# Load the new dataset
df = pd.read_csv("Data/clinical_trials_full_5000.csv")

print("=== DATASET OVERVIEW ===")
print("Total trials:", len(df))
print("Unique NCT numbers:", df["NCT Number"].nunique())
print("Number of columns:", len(df.columns))

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== MISSING VALUES ===")
print(df.isna().sum())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== STUDY STATUS ===")
print(df["Study Status"].value_counts(dropna=False))

print("\n=== ENROLLMENT SUMMARY ===")
print(df["Enrollment"].describe())

print("\n=== DUPLICATE NCT NUMBERS ===")
print(df["NCT Number"].duplicated().sum())

##check largest trials
print("\n=== TOP 5 TRIALS BY ENROLLMENT ===")

top_trials = df.nlargest(5, "Enrollment")[
    ["NCT Number", "Study Title", "Enrollment"]
]

print(top_trials.to_string(index=False))

##enrollment check : actual or estimated
"Enrollment": design.get("enrollmentInfo", {}).get("count"),