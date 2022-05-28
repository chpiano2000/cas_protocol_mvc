from datetime import datetime
import requests
import xmltodict
import json
from requests.auth import HTTPBasicAuth

from app.config import (
    BASE_URL,
    BASIC_AUTH_PASSWORD,
    BASIC_AUTH_USERNAME,
    STAGING_VALIDATE_URL,
)


def check_token_expired(time: datetime):
    if datetime.now() > time:
        return True
    else:
        return False


def xml_to_json(xml_res):
    xpars = xmltodict.parse(xml_res)
    return xpars


def validate_ticket(ticket: str):
    url = f"{STAGING_VALIDATE_URL}?ticket={ticket}&service={BASE_URL}/home"

    headers = {"Authorization": "Basic ZGV2dGVhbTpEZXZUZWFtVmNjMTIzKio="}
    response = requests.request("GET", url, headers=headers)

    # response = requests.request("GET", url)
    return xml_to_json(response.content)
