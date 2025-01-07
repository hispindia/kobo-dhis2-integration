
import requests
from utils import log_info, log_error
from constants import DHIS2_BASE_URL, DHIS2_USERNAME, DHIS2_PASSWORD

def check_existing_entry(kobo_id, program_id):
    try:
        search_url = f"{DHIS2_BASE_URL}/trackedEntityInstances.json"
        params = {
            "program": program_id,
            "ouMode": "DESCENDANTS",
            "filter": f"aU65d6OJSGv:eq:{kobo_id}",
        }
        response = requests.get(search_url, auth=(DHIS2_USERNAME, DHIS2_PASSWORD), params=params)
        if response.status_code == 200:
            return len(response.json().get("trackedEntityInstances", [])) > 0
        else:
            log_error(f"Error fetching entry: {response.status_code}")
            return False
    except Exception as e:
        log_error(f"Exception during entry check: {e}")
        return False

def push_to_dhis2(tracker_data):
    try:
        response = requests.post(
            f"{DHIS2_BASE_URL}/trackedEntityInstances",
            json=tracker_data,
            auth=(DHIS2_USERNAME, DHIS2_PASSWORD),
        )
        if response.status_code == 200:
            log_info("Data successfully pushed to DHIS2.")
        else:
            log_error(f"Failed to push data. Status code: {response.status_code}, Response: {response.content}")
    except Exception as e:
        log_error(f"Error while pushing to DHIS2: {e}")
