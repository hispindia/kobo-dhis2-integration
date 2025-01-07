# README: KOBO Event Integration

## Overview
This project facilitates the integration of gender perception survey data from KoboToolbox to DHIS2 as events. It modularizes the logic into specific files for better scalability and maintainability.

## File Structure

- **constants.py**: Contains API credentials, URLs, and configuration constants.
- **utils.py**: Provides logging utilities for streamlined error and info logging.
- **mapping.py**: Includes mapping definitions for data transformations.
- **integration.py**: Handles DHIS2 interactions for fetching and pushing events.
- **main.py**: Orchestrates the entire process from data fetching to event creation.

## Workflow
1. **Fetch Data**: Retrieve survey data from KoboToolbox using its API.
2. **Mapping**: Map Kobo data fields to DHIS2 data elements.
3. **Validation**: Verify existing tracked entity instances (TEIs) in DHIS2.
4. **Event Creation**: Create and push events to DHIS2.
5. **Logging**: Log all operations and errors for audit and debugging purposes.

## Setup and Usage

### Prerequisites
- Python 3.8 or higher.

### Configuration
- Update credentials and API details in `constants.py`.

### Running the Script
Execute the main script:
```bash
python main.py
```

## Logging
- Logs are stored in `gender_perception.log`.
- Logs include info messages for successful operations and error details for failures.

