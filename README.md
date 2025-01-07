# README: KOBO-DHIS2 Integration for Enrollment & Events

## Overview
This repository provides scripts to integrate data from KoboToolbox into DHIS2. It supports two types of integrations:
1. **Enrollment**: Tracks entity enrollments and their attributes.
2. **Events**: Captures gender perception survey responses as DHIS2 events.

## Features
- **Data Fetching**: Retrieve data from KoboToolbox using its API.
- **Mapping**: Convert KoboToolbox fields into DHIS2 attributes and data elements.
- **Event Creation**: Push data to DHIS2 as enrollment or program stage events.
- **Modular Design**: Code is structured for scalability and maintainability.
- **Logging**: Logs all operations and errors for transparency and debugging.

## Structure
- **Enrollment**: Scripts handle entity registration, attribute mapping, and enrollments.
- **Events**: Scripts handle survey data mapping and event creation.

## Setup
1. Update credentials and configuration in `constants.py`.

## Usage
- **Run Enrollment Events Integration**:
  ```bash
  python main.py under enrollment branch
  ```
- **Run Gender Perception Events Integration**:
  ```bash
  python main.py under event branch
  ```

## Logging
Logs are stored in separate files named after the enrollment/event script

