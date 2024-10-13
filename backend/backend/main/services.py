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
from .config import \
    get_booking_text, \
    TIME_SLOT_DICT, \
    ADMIN_FOOTER_INFO


async def make_auth_request(token):
    # web_address = "https://localhost"
    # web_address = "https://127.0.0.1"
    web_address = "https://mipt.site"

    log(f"Начало запроса к сервису авторизации. T:{token}, W:{web_address}", "i")

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    log(f"Сделан запрос к сервису авторизации с токеном. T:{token}", "i")

    response = session.get(
        web_address + ':8088/get-info/',
        verify=False,
        headers={"Accept": "application/json",
                 "Authorization": f"Token {token}"})
    response.encoding = 'utf-8'
    return response.json()


def update_email(username: str, new_email: str):
    try:
        user_wallet = UsersWallet.objects.get(username=username)
        user_wallet.email = new_email
        user_wallet.save()
        log(f"Почта кошелька обновлена. Новая почта: {user_wallet.email}.", "i")
    except Exception as e:
        log(f"Ошибка в обновлении почты. Error:{e}", "e")


async def check_token(token: str):
    response = asyncio.create_task(make_auth_request(token))

    res = await asyncio.gather(response)

    if res[0].get("detail", "") == "Invalid token header. Token string should not contain spaces." or \
            res[0].get("detail", "") == "Invalid token.":
        log(f"Запрос на авторизацию неудачен. E:{res[0]}", "e")
        return {
            "result": False,
            "value": res[0]
        }
    else:
        log(f"Запрос на авторизацию успешен. R:{res[0]}", "i")
        return {
            "result": True,
            "value": res[0]
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
        email: str,
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
        email_address = email # get_email_by_username(user)  "kristal.as@phystech.edu"
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


# BOOKING ITERATION


def get_queue_item(booking) -> dict:
    return {
        "audience": booking.audience,
        "audience_number": booking.audience.number,
        "user_wallet": booking.user,
        "number_bb": booking.number_bb,
        "pair_number": booking.pair_number,
        "time_slot": booking.time_slot,
        "status": "Ожидание" # 0-Ожидание 1-Принято 2-Отклонено
    }


def check_booking_availability(booking, time_slot):
    if booking.time_slot <= time_slot <= booking.time_slot + booking.pair_number:
        return True
    return False


def make_queue_list(time_slot: int):
    all_booking = Book.objects.all()
    result_queue = []
    for booking in all_booking:
        if check_booking_availability(booking, time_slot):
            result_queue.append(get_queue_item(booking))
    return result_queue


def time_slot_to_time(slot_number):
    slot_dict = TIME_SLOT_DICT
    return slot_dict[slot_number]


def get_confirmation_text(queue_item, username):
    return f"Уважаемый, {username}\n\n" \
           f"Сообщаем Вам, что бронирование аудитории {queue_item['audience'].number} прошло успешно\n" \
           f"\n\tНомер аудитории: {str(queue_item['audience'])}\n" \
           f"\tВремя бронирования: {time_slot_to_time(queue_item['time_slot'])}\n" \
           f"\tОбщая продолжительность: {queue_item['pair_number']}\n" \
           f"\tСписанные баллы бронирования: {queue_item['number_bb']} ББ {ADMIN_FOOTER_INFO}"


def get_reject_text(
        queue_item,
        username,
        queue_number,
        queue_len,
        places_number,
        min_bb_number):
    return f"Уважаемый, {username}\n\n" \
           f"Сообщаем Вам, что бронирование аудитории {queue_item['audience'].number} НЕ ПРОШЛО\n" \
           f"\nВаш номер в очереди: {queue_number}\n" \
           f"Общая длина очереди: {queue_len}\n" \
           f"Число доступных мест: {places_number}" \
           f"Минимально принятая заявка на бронирование: {min_bb_number}\n" \
           f"\n\tНомер аудитории: {str(queue_item['audience'])}\n" \
           f"\tВремя бронирования: {time_slot_to_time(queue_item['time_slot'])}\n" \
           f"\tОбщая продолжительность: {queue_item['pair_number']}\n" \
           f"\tСписанные баллы бронирования: 0 ББ {ADMIN_FOOTER_INFO}"


def get_end_booking(audience_number, time_slot, pair_number, number_bb, username):
    return f"Уважаемый, {username}\n\n" \
           f"Сообщаем Вам, что бронирование аудитории {audience_number} завершено. " \
           f"Просьба покинуть аудиторию или забронировать следующую\n" \
           f"\n\tНомер аудитории: {audience_number}\n" \
           f"\tВремя бронирования: {time_slot_to_time(time_slot)}\n" \
           f"\tОбщая продолжительность: {pair_number}\n" \
           f"\tСписанные баллы бронирования: {number_bb} ББ {ADMIN_FOOTER_INFO}"


def check_queue_list(time_slot: int):
    number_of_audiences = len(Audience.objects.exclude(audience_status__name='Отсутствует для бронирования'))
    queue_list = make_queue_list(time_slot)
    queue = sorted(queue_list, key=lambda item: int(item["number"]), reverse=True)

    email_list = make_email_list(queue, number_of_audiences)
    audience_list = make_audience_list(queue, number_of_audiences)

    return email_list, audience_list


def make_audience_list(queue, number_of_audiences):
    for i in range(number_of_audiences):
        if i <= number_of_audiences:
            queue[i]["status"] = "Принято"
        else:
            queue[i]["status"] = "Отклонено"

    audience_list = []
    for queue_item in queue:
        if queue_item["status"] == "Принято":
            audience_list.append(queue_item)

    return audience_list


def make_email_list(queue, number_of_audiences):
    email_list = []
    for i in range(number_of_audiences):
        if i <= number_of_audiences:
            email_list.append({
                "email": queue[i].user.email,
                "title": f"Бронирование прошло успешно | {queue[i]['audience'].number}",
                "text": get_confirmation_text(
                    queue_item=queue[i],
                    username=queue[i].user.username)})
        else:
            email_list.append({
                "email": queue[i].user.email,
                "title": f"Бронирование не удалось | {queue[i]['audience'].number}",
                "text": get_reject_text(
                    queue_item=queue[i],
                    username=queue[i].user.username,
                    queue_number=i,
                    queue_len=len(queue),
                    places_number=number_of_audiences,
                    min_bb_number=queue[min(number_of_audiences, len(queue)-1)]["number_bb"]
                )})
    return email_list


def update_audience():
    pass


def clear_audience(time_slot: int):
    audiences = Audience.objects.exclude(audience_status__name='Отсутствует для бронирования')
    for audience in audiences:
        audience.make_free(time_slot)
        audience.save()


def load_booking(audience_list):
    for audience in audience_list:
        if len(Audience.object.filter(number=audience['audience'].number)) == 1:
            this_audience = Audience.object.get(number=audience['audience'].number)
        else:
            log(f"Error: wrong loading audience: {audience['audience'].number}", "i")


def update_email_list_by_stop_booking(email_list, audience_list, time_slot):
    audiences = Audience.objects.all()
    for audience in audiences:
        if audience.audience_status.name == "Занято":
            flag = False
            for final_audience in audience_list:
                if final_audience["audience"].number == audience.number:
                    flag = True
            if flag:
                pass
            else:
                booking = Book.objects.get(audience__number=audience.number)
                audience_number = booking.audience.number
                number_bb = booking.number_bb
                username = booking.user.username
                pair_number = booking.pair_number
                email_test = \
                    get_end_booking(audience_number, time_slot, pair_number, number_bb, username)
                email_list.append({
                    "email": booking.user.email,
                    "title": f"Бронирование завершилось | {audience_number}",
                    "text": email_test
                })
    return email_list
