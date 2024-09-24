from requests.adapters import HTTPAdapter, Retry
import asyncio
from .models import Audience, UsersWallet, Book
from rest_framework.response import Response
import datetime
from rest_framework import status
import requests


async def make_auth_request(token):
    web_address = "https://localhost"
    # web_address = "https://127.0.0.1"
    # web_address = "https://mipt.site"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(
        web_address + ':8088/get-info/',
        verify=False,
        headers={"Accept": "application/json",
                 "Authorization": f"Token {token}"})
    response.encoding = 'utf-8'
    return response


async def check_token(token: str):
    #web_address = "https://127.0.0.1"
    # web_address = "https://mipt.site"
    #response = requests.get(
    #    web_address + ':8088/get-info/',
    #    verify=False,
    #    headers={"Accept": "application/json",
    #             "Authorization": f"Token {token}"})
    #response.encoding = 'utf-8'

    response = asyncio.create_task(make_auth_request(token))

    await asyncio.gather(response)

    if response.json().get("detail") == "Invalid token.":
        return {
            "result": False,
            "value": "Wrong token"
        }
    else:
        return {
            "result": True,
            "value": response.json()
        }


def get_audience_by_number(number):
    if len(Audience.objects.filter(number=number)) == 1:
        return Audience.objects.get(number=number)
    else:
        return None


def get_user_by_username(username):
    if len(UsersWallet.objects.filter(username=username)) == 1:
        return UsersWallet.objects.get(username=username)
    else:
        return None


def create_user_wallet(username):
    if len(UsersWallet.objects.filter(username=username)) != 0:
        return False
    users_wallet = UsersWallet(
        username=username,
        token=None,
        number_bb=28
    )
    users_wallet.save()
    return users_wallet


def get_timetable():
    res = []
    audiences = Audience.objects.all()
    for item in audiences:
        val = {item.number: {
            "status": item.audience_status.name,
            "day_history": item.day_history.pair,
            "date": item.day_history.date
            }
        }
        res.append(val)
    return res


def get_book_audience_response(
        number: str,
        user: str,
        number_bb: int,
        pair_number: int):
    new_book = Book(
        audience=get_audience_by_number(number),
        user=get_user_by_username(user),
        number_bb=number_bb,
        pair_number=pair_number,
        date=datetime.datetime.now().date(),
        booking_time=datetime.datetime.now().time(),
        visibility=1)
    new_book.save()
    audience = Audience.objects.get(number=number)
    if audience.day_history.pair[pair_number][1] == "Свободно":
        audience.day_history.pair[pair_number][1] = "Занято"
        audience.day_history.pair[pair_number][2] = user
        audience.day_history.pair[pair_number][3] = str(number_bb)
        audience.day_history.save()
        audience.save()
        return Response(
            {
                "result": True,
                "audience": new_book.audience.number,
                "user": new_book.user.username,
                "number_bb": number_bb,
                "pair_number": pair_number
            },
            status=status.HTTP_201_CREATED)
    else:
        return Response(
            {
                "result": False,
                "audience": new_book.audience.number,
                "status": audience.day_history.pair[pair_number][1],
                "number_bb": number_bb,
                "pair_number": pair_number
            },
            status=status.HTTP_204_NO_CONTENT)
