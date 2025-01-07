# README: DHIS2-Kobo Integration Project

## Overview
This project facilitates the integration of data between KoboToolbox and DHIS2, utilizing Python-based scripts for automation. It modularizes the code into specific files for better maintainability and scalability.

## File Structure

- **constants.py**: Contains constant values like API endpoints, credentials, and configuration details.
- **utils.py**: Includes utility functions for logging and other shared functionalities.
- **mapping.py**: Houses mapping logic for converting codes into meaningful values (e.g., partner codes, gender, region, etc.).
- **integration.py**: Handles interactions with the DHIS2 API, including checking for existing entries and pushing new data.
- **main.py**: Orchestrates the entire process, fetching data from KoboToolbox, processing it, and sending it to DHIS2.

## Workflow
1. **Fetch Data from KoboToolbox**: Data is retrieved using the Kobo API, filtered by region.
2. **Mapping**: Raw data is processed through mapping functions to prepare it for DHIS2.
3. **Validation**: Checks if the data already exists in DHIS2.
4. **Push to DHIS2**: New entries are sent to DHIS2 using the API.
5. **Logging**: All actions and errors are logged for auditing and debugging.

## Setup and Usage

### Prerequisites
- Python 3.8 or higher.


### Configuration
- Update the credentials and API endpoints in `constants.py`.

### Running the Script
Execute the main script:
```bash
python main.py
```
