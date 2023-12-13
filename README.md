# Kobo-DHIS Integration

This Python script facilitates the integration of data from KoboToolbox into DHIS2. It fetches data from KoboToolbox, transforms it, and creates Tracked Entity Instances and enrollments in DHIS2.

## Prerequisites

- Python 3.x

## Configuration

1. Set up your credentials:
   - Update `kobo_username` and `kobo_password` with your KoboToolbox credentials.
   - Update `dhis2_username` and `dhis2_password` with your DHIS2 credentials.

2. Specify the KoboToolbox form ID:
   - Set the `form_id` variable with the relevant KoboToolbox form ID.

3. Adjust other parameters:
   - Customize the DHIS2 program ID and any other parameters as needed.

## Usage

Run the script using the following command:

```bash
python kobo_dhis_integration.py
