from .models import Audience, UsersWallet, Book
from rest_framework.response import Response
import datetime
from rest_framework import status
import requests


def check_token(token: str):
    response = requests.get(
        'https://mipt.site:8088/get-info/',
        verify=False,
        headers={"Accept": "application/json",
                 "Authorization": f"Token {token}"})
    response.encoding = 'utf-8'

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


def _get_timetable():
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
        pair_number: int
):
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


def get_token(username: str, password: str):
    response = requests.post(
        'https://mipt.site:8088/token/',
        verify=False,
        json={'username':'st2257', 'password': 'miptpass'})
    response.encoding = 'utf-8'

    return response.json()
