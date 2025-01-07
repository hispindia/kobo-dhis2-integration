import requests
from constants import KOBO_BASE_URL, FORM_ID, KOBO_USERNAME, KOBO_PASSWORD, LOG_FILE, REGION_VALUE
from utils import configure_logging, log_info, log_error
from integration import check_existing_entry, push_to_dhis2
from mapping import (
    map_partner_value, map_gender_value, map_region_value,
    map_enum_value, map_country_value, map_district_value, map_training_value
)

def main():
    configure_logging(LOG_FILE)
    kobo_url = f"{KOBO_BASE_URL}/{FORM_ID}/data.json?query=%7B%22R_Registration/country%22:%22{REGION_VALUE}%22%7D"

    try:
        response = requests.get(kobo_url, auth=(KOBO_USERNAME, KOBO_PASSWORD))
        if response.status_code == 200:
            kobo_data = response.json()["results"]
            for entry in kobo_data:
                kobo_id = entry.get("R_Registration/R_ID")
                if check_existing_entry(kobo_id, "ONV44BbaETD"):
                    log_info(f"Entry {kobo_id} already exists in DHIS2.")
                    continue

                partner_name = map_partner_value(entry.get("R_Registration/partner", ""))
                region_name = map_region_value(entry.get("R_Registration/region", ""))
                gender = map_gender_value(entry.get("R_Registration/R_gender", ""))
                country = map_country_value(entry.get("R_Registration/country", ""))
                district = map_district_value(entry.get("R_Registration/district", ""))
                training = map_training_value(entry.get("R_Registration/training", ""))

                attributes = [
                    {"attribute": "zgA4ddgoriO", "value": entry.get("R_Registration/R_name", "")},
                    {"attribute": "SeuLNpCbbat", "value": gender},
                    {"attribute": "Zgi47Dql2Ei", "value": entry.get("R_Registration/R_DOB", "")},
                    {"attribute": "j5KaHRmRVWV", "value": entry.get("R_Registration/R_cal_age", "")},
                    {"attribute": "v7BW9WkxNPa", "value": country},
                    {"attribute": "uHg8el53h7I", "value": region_name},
                    {"attribute": "OlSEn9IKy3a", "value": district},
                    {"attribute": "Nsak9EagtaD", "value": partner_name},
                    {"attribute": "VTVrcCoiwNG", "value": training},
                ]

                log_info(f"Attributes prepared for {kobo_id}.")
                tracker_data = {
                    "trackedEntityType": "BVRdvpUal73",
                    "orgUnit": region_name,
                    "attributes": attributes,
                    "enrollments": [
                        {
                            "orgUnit": region_name,
                            "program": "ONV44BbaETD",
                            "enrollmentDate": entry.get("start", ""),
                        }
                    ],
                }

                push_to_dhis2(tracker_data)
        else:
            log_error(f"Failed to fetch data from Kobo. Status code: {response.status_code}")
    except Exception as e:
        log_error(f"Error during data fetching: {e}")

if __name__ == "__main__":
    main()
