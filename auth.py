
import requests
from requests.auth import HTTPBasicAuth

def get_auth(username, password):
    return HTTPBasicAuth(username, password)
