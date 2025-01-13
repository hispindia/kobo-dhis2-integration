import requests
import logging
from auth import get_auth

def fetch_teis_from_dhis2(attribute_value, dhis2_url, username, password, tracked_entity_attribute_uid):
    logging.info(f"Fetching Tracked Entity Instances for attribute value: {attribute_value}")
    tei_url = f"{dhis2_url}/trackedEntityInstances.json"
    params = {
        "program": "ONV44BbaETD",
        "ou": "NtmOjSYB6Xr",
        "ouMode": "DESCENDANTS",
        "filter": f"{tracked_entity_attribute_uid}:EQ:{attribute_value}",
        "fields": "trackedEntityInstance,orgUnit",
    }
    try:
        response = requests.get(tei_url, params=params, auth=get_auth(username, password))
        response.raise_for_status()
        teis = response.json().get("trackedEntityInstances", [])
        logging.info(f"Fetched {len(teis)} Tracked Entity Instances")
        return teis
    except Exception as e:
        logging.error(f"Error fetching Tracked Entity Instances: {e}")
        return []
