import requests
import logging
from constants import (
    KOBO_URL,
    KOBO_USERNAME,
    KOBO_PASSWORD,
    DHIS2_URL,
    DHIS2_USERNAME,
    DHIS2_PASSWORD,
    LOGGING_FILE,
    TRACKED_ENTITY_ATTRIBUTE_UID,
    PROGRAM_STAGE_ID_PRE,
)
from integration import fetch_teis_from_dhis2
from mapping import DATA_ELEMENT_MAPPING
from utils import setup_logging

def create_event_payload(tei_uid, org_unit_id, kobo_entry, data_element_mapping):
    event_payload = {
        "trackedEntityInstance": tei_uid,
        "program": "ONV44BbaETD",
        "programStage": PROGRAM_STAGE_ID_PRE,
        "orgUnit": org_unit_id,
        "eventDate": kobo_entry.get("_submission_time", ""),
        "status": "COMPLETED",
        "dataValues": []
    }

    for dhis2_uid, mapping_details in data_element_mapping.items():
        kobo_id = mapping_details.get("kobo_id", "")
        kobo_value = kobo_entry.get(kobo_id, "")
        options = mapping_details.get("options", {})

        if kobo_value in options:
            event_payload["dataValues"].append({
                "dataElement": dhis2_uid,
                "value": options[kobo_value]
            })
        elif kobo_value:
            event_payload["dataValues"].append({
                "dataElement": dhis2_uid,
                "value": kobo_value
            })

    return event_payload

def push_event_to_dhis2(event_payload, dhis2_url, username, password):
    headers = {'Content-Type': 'application/json'}
    auth = (username, password)
    url = f"{dhis2_url}/events"
    try:
        response = requests.post(url, headers=headers, auth=auth, json=event_payload)
        response.raise_for_status()
        logging.info(f"Event pushed successfully: {response.json()['response']}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            conflict_detail = response.json().get("message", "Conflict details not available.")
            logging.warning(f"Conflict occurred while pushing event: {conflict_detail}")
        else:
            logging.error(f"HTTPError while pushing event: {e}")
    except Exception as e:
        logging.error(f"Error pushing event: {e}")

def main():
    setup_logging(LOGGING_FILE)

    response = requests.get(KOBO_URL, auth=(KOBO_USERNAME, KOBO_PASSWORD))
    kobo_data = response.json().get("results", [])

    for entry in kobo_data:
        link_number_id = entry.get("link_email_ID") or entry.get("link_number_ID")
        if not link_number_id:
            logging.warning("Kobo entry is missing both link_email_ID and link_number_ID")
            continue

        logging.info(f"Processing Kobo entry with link ID: {link_number_id}")
        teis = fetch_teis_from_dhis2(link_number_id, DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD, TRACKED_ENTITY_ATTRIBUTE_UID)

        for tei in teis:
            tei_uid = tei.get("trackedEntityInstance", "")
            org_unit_id = tei.get("orgUnit", "")
            logging.info(f"Mapping Kobo link_number_ID {link_number_id} to TEI UID {tei_uid} and Org Unit ID {org_unit_id}")

            event_payload = create_event_payload(tei_uid, org_unit_id, entry, DATA_ELEMENT_MAPPING)
            push_event_to_dhis2(event_payload, DHIS2_URL, "DHIS2_USERNAME", DHIS2_PASSWORD)

if __name__ == "__main__":
    main()
