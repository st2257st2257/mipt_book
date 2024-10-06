import requests
from requests.adapters import HTTPAdapter, Retry
import asyncio


async def create_user_wallet_make(token, username):
    web_address = "https://mipt.site"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    response = session.post(
        web_address + ":8000/wallet/",
        data={
            "type":"create_user_wallet",
            "token":token,
            "username":username
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    print(response.status_code, response.reason)

    return response


async def create_user_wallet_prev(token, username):
    response = asyncio.create_task(create_user_wallet_make(token, username))

    res = await asyncio.gather(response)
    return res


def create_user_wallet(token, username):
    check_token_result = asyncio.run(create_user_wallet_prev(token, username))
    return check_token_result


def create_user_wallet_old(token, username):
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
