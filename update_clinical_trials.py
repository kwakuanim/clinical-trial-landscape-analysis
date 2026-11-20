
import subprocess
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"


def run_script(script_name):
    print(f"\nRunning {script_name}...", flush=True)

    subprocess.run(
        [sys.executable, str(BASE_DIR / script_name)],
        check=True,
        cwd=BASE_DIR
    )

    print(f"Completed: {script_name}", flush=True)


def update_powerbi_files():
    files = {
        "clinical_trials_cleaned_5000.csv":
            "clinical_trials_cleaned.csv",
        "clinical_trial_conditions_5000.csv":
            "clinical_trial_conditions.csv"
    }

    # Check all source files before replacing anything
    for source in files:
        if not (DATA_DIR / source).is_file():
            raise FileNotFoundError(source)

    for source, destination in files.items():
        shutil.copy2(
            DATA_DIR / source,
            DATA_DIR / destination
        )
        print(f"Updated: {destination}")


try:
    run_script("fetch_clinical_trials.py")
    run_script("process_clinical_trials.py")
    update_powerbi_files()

    print("\nPower BI source files updated successfully.")

except (subprocess.CalledProcessError, OSError) as error:
    print(f"\nUpdate failed: {error}")
    sys.exit(1)
