import requests
import logging

region_value = "assi"
form_id = ""
success_count = 0

kobo_url = f"https://kobo.humanitarianresponse.info/api/v2/assets/{form_id}/data.json?query=%7B%22R_Registration/region%22:%22{region_value}%22%7D"
kobo_username = ""
kobo_password = ""

dhis2_url = "https://me.yesdigital.org/yesdigital/api/trackedEntityInstances"
dhis2_username = ""
dhis2_password = ""
program_id = "ONV44BbaETD"

print("kobo_url--", kobo_url)
logging.basicConfig(filename='integration_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

kobo_response = requests.get(
    kobo_url,
    auth=(kobo_username, kobo_password)
)

if kobo_response.status_code == 200:
    kobo_data = kobo_response.json()["results"]

    for entry in kobo_data:
        district_code = entry.get("R_Registration/district", "")
        org_unit_api_url = f"https://me.yesdigital.org/yesdigital/api/organisationUnits?filter=code:eq:{district_code}&fields=[name,id,code]"

        org_unit_response = requests.get(org_unit_api_url, auth=(dhis2_username, dhis2_password))

        if org_unit_response.status_code == 200:
            org_units_data = org_unit_response.json()["organisationUnits"]

            if org_units_data:
                org_unit_id = org_units_data[0].get("id", "")
                dhis2_tracker_data = {
                    "trackedEntityType": "BVRdvpUal73",
                    "orgUnit": org_unit_id,
                    "attributes": [],
                    "enrollments": [{
                        "orgUnit": org_unit_id,
                        "program": program_id,
                        "enrollmentDate": entry["start"]
                    }]
                }

                attribute_mappings = [
                    {"attribute": "u8XxSMST3Dh", "value": entry.get("who", "")},
                    {"attribute": "SnLua4CGbSz", "value": "Yes" if entry.get("R_age_qual", "") == "1" else ""},
                    {"attribute": "xF7aLHOCibx", "value": "Yes" if entry.get("R_Registration/R_born", "") == "1" else ""},
                    # ... (rest of the attribute mappings)
                ]

                dhis2_tracker_data["attributes"].extend(attribute_mappings)

                dhis2_response = requests.post(
                    dhis2_url,
                    json=dhis2_tracker_data,
                    auth=(dhis2_username, dhis2_password),
                    headers={'Content-Type': 'application/json'}
                )

                if dhis2_response.status_code == 200:
                    print("Tracked Entity Instances and enrollments successfully created in DHIS2.")
                    success_count += 1
                    logging.info(f'Success - Tracked Entity created: {entry["_id"]}')
                else:
                    print(f"Error creating Tracked Entity Instances and enrollments in DHIS2. Status code: {dhis2_response.status_code}")
                    logging.error(f'Error creating Tracked Entity - {entry["_id"]}: {dhis2_response.text}')
        else:
            print(f"Error fetching organization unit details from DHIS2. Status code: {org_unit_response.status_code}")
            print(f"Total successful entries: {success_count}")
            logging.info(f'Total successful entries: {success_count}')

else:
    print(f"Error fetching data from KoboToolbox. Status code: {kobo_response.status_code}")
    logging.error(f'Error fetching data from KoboToolbox: {kobo_response.text}')
