##automatic retrieval of data from clinicaltrail.gov

import requests
import pandas as pd
from pathlib import Path

# API configuration
API_URL = "https://clinicaltrials.gov/api/v2/studies"
MAX_STUDIES = 5000
PAGE_SIZE = 1000

# Create output directory
output_dir = Path("Data")
output_dir.mkdir(exist_ok=True)

all_studies = []
next_page_token = None

print("Starting ClinicalTrials.gov data retrieval...")

while len(all_studies) < MAX_STUDIES:

    params = {
        "format": "json",
        "pageSize": PAGE_SIZE,
        "filter.overallStatus": "COMPLETED",
        "query.term": "AREA[StudyType]INTERVENTIONAL",
        "sort": "LastUpdatePostDate:desc"
    }

    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )
    response.raise_for_status()

    data = response.json()
    studies = data.get("studies", [])

    if not studies:
        break

    
    for study in studies:
        protocol = study.get("protocolSection", {})

        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions = protocol.get("conditionsModule", {})
        interventions = protocol.get("armsInterventionsModule", {})
        sponsor = protocol.get("sponsorCollaboratorsModule", {})
        eligibility = protocol.get("eligibilityModule", {})
        outcomes = protocol.get("outcomesModule", {})
        description = protocol.get("descriptionModule", {})

        nct = identification.get("nctId", "")

        def join_values(values):
            return "|".join(str(v) for v in (values or []))

        def outcome_titles(key):
            return join_values([
                item.get("measure", "")
                for item in outcomes.get(key, [])
            ])

        all_studies.append({
            "NCT Number": nct,
            "Study Title": identification.get("briefTitle", ""),
            "Study URL": f"https://clinicaltrials.gov/study/{nct}",
            "Study Status": status.get("overallStatus", ""),
            "Study Results": status.get("resultsFirstPostDateStruct", {}).get("date", ""),
            "Conditions": join_values(conditions.get("conditions")),
            "Interventions": join_values([
                item.get("name", "")
                for item in interventions.get("interventions", [])
            ]),
            # Extract intervention types for clinical trial classification
            "Intervention Types": join_values([
             item.get("type", "")
             for item in interventions.get("interventions", [])
             ]),
            "Primary Outcome Measures": outcome_titles("primaryOutcomes"),
            "Secondary Outcome Measures": outcome_titles("secondaryOutcomes"),
            "Other Outcome Measures": outcome_titles("otherOutcomes"),
            "Sponsor": sponsor.get("leadSponsor", {}).get("name", ""),
            "Collaborators": join_values([
                item.get("name", "")
                for item in sponsor.get("collaborators", [])
            ]),
            "Sex": eligibility.get("sex", ""),
            "Age": eligibility.get("stdAges", []),
            "Phases": join_values(design.get("phases")),
            "Enrollment": design.get("enrollmentInfo", {}).get("count"),
            "Enrollment Type": design.get("enrollmentInfo", {}).get("type", ""),
            "Funder Type": sponsor.get("leadSponsor", {}).get("class", ""),
            "Study Type": design.get("studyType", ""),
            "Start Date": status.get("startDateStruct", {}).get("date", ""),
            "Primary Completion Date": status.get(
                "primaryCompletionDateStruct", {}
            ).get("date", ""),
            "Completion Date": status.get(
                "completionDateStruct", {}
            ).get("date", ""),
            "Locations": join_values([
                item.get("country", "")
                for item in protocol.get(
                    "contactsLocationsModule", {}
                ).get("locations", [])
            ])
        })

        if len(all_studies) >= MAX_STUDIES:
            break


    print(f"Retrieved {len(all_studies)} studies")

    next_page_token = data.get("nextPageToken")

    if not next_page_token:
        break

# Convert to DataFrame
df = pd.DataFrame(all_studies)

# Remove duplicates
df = df.drop_duplicates(subset=["NCT Number"])

# Save raw API data
output_file = output_dir / "clinical_trials_full_5000.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nDownload completed!")
print(f"Total unique studies: {len(df)}")
print(f"Saved to: {output_file}")


