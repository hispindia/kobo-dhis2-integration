from datetime import datetime
import os

auth_file = "auth.enc"
if os.path.exists(auth_file):
    with open(auth_file) as f:
        auth_data = dict(line.strip().split('=') for line in f if '=' in line)
else:
    raise FileNotFoundError("Authentication file not found!")

# Kobo API Details
KOBO_BASE_URL = "https://kobo.humanitarianresponse.info/api/v2/assets"
KOBO_USERNAME = auth_data.get("KOBO_USERNAME")
KOBO_PASSWORD = auth_data.get("KOBO_PASSWORD")

# DHIS2 API Details
DHIS2_BASE_URL = "https://me.yesdigital.org/yesdigital/api"
DHIS2_USERNAME = auth_data.get("DHIS2_USERNAME")
DHIS2_PASSWORD = auth_data.get("DHIS2_PASSWORD")

# Other constants
FORM_ID = ""
LOG_FILE = datetime.now().strftime("%Y-%m-%d") + "_integration.log"
PROGRAM_ID = "ONV44BbaETD"
