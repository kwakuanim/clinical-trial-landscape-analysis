
"""
Clinical Trial Landscape Analysis
Automated Data Pipeline

Usage:
    python update_clinical_trials.py --refresh

Pipeline:
    1. Fetch clinical trial records
    2. Validate raw data
    3. Process clinical trials
    4. Generate figures
    5. Update Power BI CSV files
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

SCRIPTS = [
    "fetch.py",
    "validate_clinical_trials.py",
    "process_clinical_trials.py",
    "explore.py"
]

POWERBI_FILES = {
    "clinical_trials_cleaned_5000.csv":
        "clinical_trials_cleaned.csv",

    "clinical_trial_conditions_5000.csv":
        "clinical_trial_conditions.csv"
}


def run_script(script_name):
    """Execute a Python script in the project directory."""

    script_path = BASE_DIR / script_name

    if not script_path.is_file():
        raise FileNotFoundError(
            f"Required script not found: {script_path}"
        )

    print(
        f"\nRunning {script_name}...",
        flush=True
    )

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
        cwd=BASE_DIR
    )

    print(
        f"Completed: {script_name}",
        flush=True
    )


def update_powerbi_files():
    """Copy processed datasets to Power BI source files."""

    print("\nUpdating Power BI source files...")

    # Check all sources before copying
    for source in POWERBI_FILES:
        source_path = DATA_DIR / source

        if not source_path.is_file():
            raise FileNotFoundError(
                f"Missing processed dataset: {source_path}"
            )

    for source, destination in POWERBI_FILES.items():

        source_path = DATA_DIR / source
        destination_path = DATA_DIR / destination

        shutil.copy2(
            source_path,
            destination_path
        )

        print(f"Updated: {destination}")


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Refresh ClinicalTrials.gov data, "
            "regenerate figures, and update Power BI files."
        )
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "Retrieve new clinical trial data and "
            "replace existing processed datasets."
        )
    )

    args = parser.parse_args()

    if not args.refresh:
        print(
            "\nNo files have been changed.\n"
            "To refresh the dataset, run:\n\n"
            "python update_clinical_trials.py --refresh"
        )
        return

    print("\n" + "=" * 60)
    print("CLINICAL TRIAL DATA PIPELINE")
    print("=" * 60)

    # Check all required scripts before starting
    for script in SCRIPTS:
        if not (BASE_DIR / script).is_file():
            raise FileNotFoundError(
                f"Required script missing: {script}"
            )

    # Run the complete pipeline
    for script in SCRIPTS:
        run_script(script)

    # Update files used by Power BI
    update_powerbi_files()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nOutputs:")
    print("- Raw clinical trial dataset")
    print("- Cleaned clinical trial dataset")
    print("- Clinical trial conditions dataset")
    print("- Updated analytical figures")
    print("- Updated Power BI source CSV files")


if __name__ == "__main__":

    try:
        main()

    except (
        subprocess.CalledProcessError,
        OSError
    ) as error:

        print(
            f"\nPipeline failed: {error}",
            file=sys.stderr
        )

        sys.exit(1)
