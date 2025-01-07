import requests
from constants import KOBO_URL, KOBO_USERNAME, KOBO_PASSWORD, DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD, TRACKED_ENTITY_ATTRIBUTE_UID
from utils import configure_logging, log_info, log_error
from integration import fetch_teis_from_dhis2, push_event_to_dhis2
from mapping import data_element_mapping

def main():
    configure_logging("gender_perception.log")
    try:
        response = requests.get(KOBO_URL, auth=(KOBO_USERNAME, KOBO_PASSWORD))
        response.raise_for_status()
        kobo_data = response.json().get("results", [])
        for kobo_entry in kobo_data:
            link_number_id = kobo_entry.get("link_email_ID") or kobo_entry.get("link_number_ID")
            if not link_number_id:
                log_error("Missing link_email_ID and link_number_ID in Kobo entry")
                continue
            
            teis = fetch_teis_from_dhis2(link_number_id, DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD, TRACKED_ENTITY_ATTRIBUTE_UID)
            for tei in teis:
                tei_uid = tei["trackedEntityInstance"]
                org_unit_id = tei["orgUnit"]
                event_payload = {
                    "trackedEntityInstance": tei_uid,
                    "program": "ONV44BbaETD",
                    "programStage": "dYIOHYPQ41c",
                    "orgUnit": org_unit_id,
                    "eventDate": kobo_entry.get("_submission_time", ""),
                    "status": "COMPLETED",
                    "dataValues": []
                }
                push_event_to_dhis2(event_payload, DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD)
    except Exception as e:
        log_error(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
