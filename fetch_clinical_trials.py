
"""
Clinical Trial Landscape Analysis
Automated ClinicalTrials.gov Data Retrieval

Retrieves up to 5,000 completed interventional studies
from the ClinicalTrials.gov API.

Output:
    Data/clinical_trials_full_5000.csv

Author: Manfred Anim
"""

import time
from pathlib import Path

import pandas as pd
import requests


# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

API_URL = "https://clinicaltrials.gov/api/v2/studies"

MAX_STUDIES = 5000
PAGE_SIZE = 1000

OUTPUT_FILE = DATA_DIR / "clinical_trials_full_5000.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def join_values(values):
    """Join multiple values into a pipe-separated string."""

    return "|".join(
        str(value)
        for value in (values or [])
        if value is not None
    )


def get_outcome_titles(outcomes, key):
    """Extract outcome measure titles."""

    return join_values([
        item.get("measure", "")
        for item in outcomes.get(key, [])
    ])


def fetch_page(session, params, max_retries=3):
    """Retrieve one API page with retry handling."""

    for attempt in range(1, max_retries + 1):

        try:
            response = session.get(
                API_URL,
                params=params,
                timeout=60
            )

            response.raise_for_status()

            return response.json()

        except (
            requests.RequestException,
            ValueError
        ) as error:

            print(
                f"Request attempt {attempt} failed: {error}"
            )

            if attempt == max_retries:
                raise

            time.sleep(2 ** attempt)


# ============================================================
# 3. EXTRACT CLINICAL TRIAL INFORMATION
# ============================================================

def extract_study(study):
    """Extract selected study fields from an API record."""

    protocol = study.get("protocolSection", {})

    identification = protocol.get(
        "identificationModule", {}
    )

    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})

    conditions = protocol.get(
        "conditionsModule", {}
    )

    interventions = protocol.get(
        "armsInterventionsModule", {}
    )

    sponsor = protocol.get(
        "sponsorCollaboratorsModule", {}
    )

    eligibility = protocol.get(
        "eligibilityModule", {}
    )

    outcomes = protocol.get(
        "outcomesModule", {}
    )

    locations = protocol.get(
        "contactsLocationsModule", {}
    )

    nct = identification.get("nctId", "")

    intervention_records = interventions.get(
        "interventions", []
    )

    enrollment_info = design.get(
        "enrollmentInfo", {}
    )

    lead_sponsor = sponsor.get(
        "leadSponsor", {}
    )

    return {
        "NCT Number": nct,

        "Study Title": identification.get(
            "briefTitle", ""
        ),

        "Study URL": (
            f"https://clinicaltrials.gov/study/{nct}"
        ),

        "Study Status": status.get(
            "overallStatus", ""
        ),

        "Study Results": status.get(
            "resultsFirstPostDateStruct", {}
        ).get("date", ""),

        "Conditions": join_values(
            conditions.get("conditions")
        ),

        "Interventions": join_values([
            item.get("name", "")
            for item in intervention_records
        ]),

        "Intervention Types": join_values([
            item.get("type", "")
            for item in intervention_records
        ]),

        "Primary Outcome Measures": get_outcome_titles(
            outcomes,
            "primaryOutcomes"
        ),

        "Secondary Outcome Measures": get_outcome_titles(
            outcomes,
            "secondaryOutcomes"
        ),

        "Other Outcome Measures": get_outcome_titles(
            outcomes,
            "otherOutcomes"
        ),

        "Sponsor": lead_sponsor.get(
            "name", ""
        ),

        "Collaborators": join_values([
            item.get("name", "")
            for item in sponsor.get("collaborators", [])
        ]),

        "Sex": eligibility.get("sex", ""),

        "Age": eligibility.get(
            "stdAges", []
        ),

        "Phases": join_values(
            design.get("phases")
        ),

        "Enrollment": enrollment_info.get(
            "count"
        ),

        "Enrollment Type": enrollment_info.get(
            "type", ""
        ),

        "Funder Type": lead_sponsor.get(
            "class", ""
        ),

        "Study Type": design.get(
            "studyType", ""
        ),

        "Start Date": status.get(
            "startDateStruct", {}
        ).get("date", ""),

        "Primary Completion Date": status.get(
            "primaryCompletionDateStruct", {}
        ).get("date", ""),

        "Completion Date": status.get(
            "completionDateStruct", {}
        ).get("date", ""),

        "Locations": join_values([
            item.get("country", "")
            for item in locations.get("locations", [])
        ])
    }


# ============================================================
# 4. RETRIEVE CLINICAL TRIALS
# ============================================================

def main():

    print("\n=== CLINICALTRIALS.GOV DATA RETRIEVAL ===")

    all_studies = []
    seen_nct_ids = set()
    seen_page_tokens = set()

    next_page_token = None
    page_number = 0

    session = requests.Session()

    try:
        while len(all_studies) < MAX_STUDIES:

            params = {
                "format": "json",
                "pageSize": PAGE_SIZE,
                "filter.overallStatus": "COMPLETED",
                "query.term": (
                    "AREA[StudyType]INTERVENTIONAL"
                ),
                "sort": "LastUpdatePostDate:desc"
            }

            if next_page_token:
                params["pageToken"] = next_page_token

            data = fetch_page(
                session,
                params
            )

            page_number += 1

            studies = data.get("studies", [])

            if not studies:
                print("No additional studies returned.")
                break

            for study in studies:

                record = extract_study(study)

                nct = record["NCT Number"]

                # Skip records with missing identifiers
                if not nct:
                    continue

                # Skip duplicate NCT identifiers
                if nct in seen_nct_ids:
                    continue

                # Verify study selection
                if record["Study Status"] != "COMPLETED":
                    continue

                if record["Study Type"] != "INTERVENTIONAL":
                    continue

                seen_nct_ids.add(nct)
                all_studies.append(record)

                if len(all_studies) >= MAX_STUDIES:
                    break

            print(
                f"Page {page_number}: "
                f"{len(all_studies):,} unique studies retrieved"
            )

            if len(all_studies) >= MAX_STUDIES:
                break

            next_page_token = data.get(
                "nextPageToken"
            )

            if not next_page_token:
                print("No further pages available.")
                break

            if next_page_token in seen_page_tokens:
                raise RuntimeError(
                    "Repeated pagination token detected."
                )

            seen_page_tokens.add(
                next_page_token
            )

    finally:
        session.close()

    # ========================================================
    # 5. CREATE DATAFRAME
    # ========================================================

    if not all_studies:
        raise RuntimeError(
            "No clinical trial records were retrieved."
        )

    df = pd.DataFrame(all_studies)

    # Final validation
    if df["NCT Number"].isna().any():
        raise ValueError(
            "Missing NCT identifiers detected."
        )

    if not df["NCT Number"].is_unique:
        raise ValueError(
            "Duplicate NCT identifiers detected."
        )

    if not df["Study Status"].eq("COMPLETED").all():
        raise ValueError(
            "Non-completed studies detected."
        )

    if not df["Study Type"].eq("INTERVENTIONAL").all():
        raise ValueError(
            "Non-interventional studies detected."
        )

    # ========================================================
    # 6. SAVE DATASET
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ========================================================
    # 7. SUMMARY
    # ========================================================

    print("\n=== DOWNLOAD COMPLETE ===")

    print("Pages retrieved:", page_number)
    print("Total unique studies:", len(df))
    print("Dataset columns:", len(df.columns))

    print(
        "Missing enrollment:",
        df["Enrollment"].isna().sum()
    )

    print(
        "Missing intervention types:",
        df["Intervention Types"].eq("").sum()
    )

    print(
        "Missing phases:",
        df["Phases"].eq("").sum()
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)

    if len(df) < MAX_STUDIES:
        print(
            f"\nWARNING: Retrieved {len(df):,} studies "
            f"instead of the target {MAX_STUDIES:,}."
        )


if __name__ == "__main__":
    main()
