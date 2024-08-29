import os
from dotenv import load_dotenv
import api_client_base as api_client

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
LM_COMPANY = os.getenv("LM_COMPANY")
LM_API_KEY = os.getenv("LM_API_KEY")
LM_ACCESS_KEY = os.getenv("LM_ACCESS_KEY")


def simple_get(lm, path, params=None):
    """
    Simple get request to the LogicMonitor API
    """
    response = lm.get(path=path, params=params)
    return response


def get_all(lm, path, params=None):
    """
    Get all items from the LogicMonitor API
    """
    response = lm.get(path=path, all=True, params=params)
    return response


# instantiate the logicmonitor api client
lm = api_client.api_logicmonitor(LM_COMPANY, LM_API_KEY, LM_ACCESS_KEY)

# params
params = {"size": 1000, "fields": "id,displayName"}

# get the first 1000 devices
response = simple_get(lm, "/device/devices", params)

# get all devices
all_devices = get_all(lm, "/device/devices", params)
