import requests
from requests.adapters import HTTPAdapter, Retry
import asyncio
import logging
import datetime
from django.conf import settings
EMAIL_KEY = settings.EMAIL_KEY


async def create_user_wallet_make(token, user, request_type="create_user_wallet"):
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
            "email_key": EMAIL_KEY,
            "type":request_type,
            "token":token,
            "username":user.username,
            "email":user.email
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Кошелёк создан. U:{user.username}, T:{token}", "i")

    print(response.status_code, response.reason)

    return response


async def create_user_wallet_prev(token, user, request_type="create_user_wallet"):
    response = asyncio.create_task(create_user_wallet_make(token, user, request_type))

    res = await asyncio.gather(response)
    return res


def create_user_wallet(token, user, request_type="create_user_wallet"):
    check_token_result = asyncio.run(create_user_wallet_prev(token, user, request_type))
    return check_token_result


async def send_email_make(email_address, email_text, email_title):
    web_address = "https://mipt.site"
    # web_address = "https://127.0.0.1"
    # web_address = "https://localhost"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    response = session.post(
        web_address + ":8083/send_email/",
        data={
            "email_key": EMAIL_KEY,
            "type":"send_email",
            "email_address":email_address,
            "email_text":email_text,
            "email_title": email_title
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Email отправлен. A:{email_address}, T:{email_title}", "i")

    return response


async def send_email_prev(email_address, email_text, email_title):
    response = asyncio.create_task(send_email_make(email_address, email_text, email_title))

    res = await asyncio.gather(response)
    return res


def send_email(email_address, email_text, email_title):
    send_email_result = asyncio.run(send_email_prev(email_address, email_text, email_title))
    return send_email_result


def log(string, log_type="w"):
    _ = f"{str(datetime.datetime.now())[:-7]} {string}"
    match log_type:
        case "d":
            logging.debug(_)
        case "i":
            logging.info(_)
        case "w":
            logging.warning(_)
        case "e":
            logging.error(_)
        case "c":
            logging.critical(_)
        case __:
            logging.debug(_)
