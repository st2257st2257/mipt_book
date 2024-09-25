import requests
from requests.adapters import HTTPAdapter, Retry

def create_user_wallet(token, username):
    web_address = "https://127.0.0.1"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    response = session.get(
        web_address + ':8088/get-info/',
        verify=False,
        headers={"Accept": "application/json",
                 "Authorization": f"Token {token}"})
    response.encoding = 'utf-8'
    return response.json()
