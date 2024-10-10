from requests.adapters import HTTPAdapter, Retry
import asyncio
from .models import Audience, UsersWallet, Book, AudienceStatus
from rest_framework.response import Response
import datetime
from rest_framework import status
import requests
import json
import logging
import datetime
from .config import get_booking_text


async def make_auth_request(token):
    # web_address = "https://localhost"
    # web_address = "https://127.0.0.1"
    web_address = "https://mipt.site"

    log(f"Начало запроса к сервису авторизации. T:{token}, W:{web_address}", "d")

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    log(f"Сделан запрос к сервису авторизации с токеном. T:{token}", "d")

    response = session.get(
        web_address + ':8088/get-info/',
        verify=False,
        headers={"Accept": "application/json",
                 "Authorization": f"Token {token}"})
    response.encoding = 'utf-8'
    return response.json()


async def check_token(token: str):
    response = asyncio.create_task(make_auth_request(token))

    res = await asyncio.gather(response)

    if res[0].get("detail", "") == "Invalid token header. Token string should not contain spaces.":
        log(f"Запрос на авторизацию неудачен. E:{res[0]}", "w")
        return {
            "result": False,
            "value": res[0]
        }
    else:
        log(f"Запрос на авторизацию успешен. R:{res[0]}", "d")
        return {
            "result": True,
            "value": res[0]
        }


def check_token_old(token: str):
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


def get_audience_by_number(number):
    if len(Audience.objects.filter(number=number)) == 1:
        log(f"Запрос на получение аудитории. A:{number}", "d")
        return Audience.objects.get(number=number)
    else:
        log(f"Запрос на получение аудитории неуспешен. A:{number}", "d")
        return None


def get_user_by_username(username):
    if len(UsersWallet.objects.filter(username=username)) == 1:
        log(f"Запрос на получение пользователя. U:{username}", "d")
        return UsersWallet.objects.get(username=username)
    else:
        log(f"Запрос на получение пользователя неуспешен. U:{username}", "w")
        return None


def get_username_by_username(username): 
    if len(UsersWallet.objects.filter(username=username)) == 1:
        log(f"Запрос на получение пользователя. U:{username}", "d")
        return UsersWallet.objects.get(username=username)
    else:
        log(f"Запрос на получение пользователя неуспешен. U:{username}", "w")
        return None


def create_user_wallet(username, token=""):
    log(f"Начало создания кошелька пользователя. U:{username}, T{token}", "d")
    if len(UsersWallet.objects.filter(username=username)) != 0:
        log(f"При создании кошелька пользователь не был найден. U:{username}", "e")
        return False
    users_wallet = UsersWallet(
        username=username,
        token=token,
        number_bb=28
    )
    users_wallet.save()
    log(f"Кошелёк пользователя успешно создан. U:{username}", "d")
    return users_wallet


def get_timetable():
    log(f"Получение расписания бронирования.", "d")
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
        log(f"Изменена дневная история. A:{number}, P:{pair_number}", "d")
        audience.day_history.pair[pair_number][2] = user
        log(f"Изменён пользователь дневной истории. A:{number}, U:{user}", "d")
        audience.day_history.pair[pair_number][3] = str(number_bb)
        log(f"Изменены баллы бронирования дневной истории. A:{number}, BB:{number_bb}", "d")
        audience.audience_status = AudienceStatus.objects.get(name="Занято")
        audience.audience_status.save()
        log(f"Статус занятости сохранён. A:{number}", "d")
        audience.day_history.save()
        log(f"Дневная история сохранена. A:{number}", "d")
        audience.save()
        log(f"Аудитория сохранена. A:{number}", "d")
        log(f"Audience booked. "
            f"A:{new_book.audience.number}, "
            f"U:{new_book.user.username}, "
            f"P:{pair_number} "
            f"BB:{number_bb}", "i")

        # Собираем данные для отправки email сообщения
        email_address = "kristal.as@phystech.edu" # get_email_by_username(user)  "kristal.as@phystech.edu"
        email_text = get_booking_text(
            username=user,
            pair_number=pair_number,
            audience=number,
            number_bb=number_bb)
        email_title = f"Бронирование аудитории {number}ГК"
        send_email(email_address, email_text, email_title)

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
        log(f"Audience already booked. A:{number}", "w")
        return Response(
            {
                "result": False,
                "audience": new_book.audience.number,
                "status": audience.day_history.pair[pair_number][1],
                "number_bb": number_bb,
                "pair_number": pair_number
            },
            status=status.HTTP_204_NO_CONTENT)


def get_email_by_username(username: str):
    user = get_username_by_username(username)
    if user is not None:
        return get_username_by_username(username).email
    else:
        return "askristal@gmail.com"


def log(string, log_type="w"):
    _ = f"{str(datetime.datetime.now())[:-7]} {string}"
    if log_type == "d":
        logging.debug(_)
    elif log_type == "i":
        logging.info(_)
    elif log_type == "w":
        logging.warning(_)
    elif log_type == "e":
        logging.error(_)
    elif log_type == "c":
        logging.critical(_)
    else:
        logging.debug(_)
