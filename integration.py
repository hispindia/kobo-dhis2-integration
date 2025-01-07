
import requests
from utils import log_info, log_error

def fetch_teis_from_dhis2(attribute_value, dhis2_url, username, password, tracked_entity_attribute_uid):
    log_info(f"Fetching TEIs from DHIS2 for attribute value: {attribute_value}")
    url = f"{dhis2_url}/trackedEntityInstances.json"
    params = {
        "program": "ONV44BbaETD",
        "ou": "NtmOjSYB6Xr",
        "ouMode": "DESCENDANTS",
        "filter": f"{tracked_entity_attribute_uid}:EQ:{attribute_value}",
        "fields": "trackedEntityInstance,orgUnit",
    }
    try:
        response = requests.get(url, params=params, auth=(username, password))
        response.raise_for_status()
        teis = response.json().get("trackedEntityInstances", [])
        log_info(f"Fetched {len(teis)} TEIs from DHIS2")
        return teis
    except Exception as e:
        log_error(f"Error fetching TEIs from DHIS2: {e}")
        return []

def push_event_to_dhis2(event_payload, dhis2_url, username, password):
    url = f"{dhis2_url}/events"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=event_payload, headers=headers, auth=(username, password))
        response.raise_for_status()
        log_info(f"Event pushed successfully: {response.json().get('response')}")
    except requests.exceptions.HTTPError as e:
        log_error(f"HTTPError pushing event: {e}")
    except Exception as e:
        log_error(f"Error pushing event: {e}")
