from requests.adapters import HTTPAdapter, Retry
import asyncio
from .models import \
    Audience, \
    UsersWallet, \
    Book, \
    AudienceStatus, \
    MarkedBusy, \
    MarkedBooked
from rest_framework.response import Response
import datetime
from rest_framework import status
import requests
import json
import logging
import datetime
from django.utils import timezone
from datetime import timedelta
from .config import \
    get_booking_text, \
    TIME_SLOT_DICT, \
    ADMIN_FOOTER_INFO, \
    TIME_SLOT_ARR
from django.conf import settings
EMAIL_KEY = settings.EMAIL_KEY
from collections import namedtuple


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
        users_len = UsersWallet.objects.filter(username=username)
        if len(users_len) == 1:
            user_wallet = UsersWallet.objects.get(username=username)
            user_wallet.email = new_email
            user_wallet.save()
            log(f"Почта кошелька обновлена. Новая почта: {user_wallet.email}.", "i")
        else:
            log(f"Ошибка в обновлении почты: username='{username}' len(users)={users_len}", "e")
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


async def send_email_make_booking(email_address, email_text, email_title, user_name, aud_name, start_time, end_time, pair_number, bb_number, preferences_list):
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
        web_address + ":8083/send_email_booking/",
        data={
            "email_key": EMAIL_KEY,
            "type":"send_email",
            "email_address": email_address,
            "email_text": email_text,
            "email_title": email_title,
            "user_name": user_name,
            "aud_name": aud_name,
            "start_time": start_time,
            "end_time": end_time,
            "pair_number": pair_number,
            "bb_number": bb_number,
            "preferences_list": preferences_list
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Email отправлен. A:{email_address}, T:{email_title}", "i")

    return response


async def send_email_prev_booking(email_address, email_text, email_title, user_name, aud_name, start_time, end_time, pair_number, bb_number, preferences_list):
    response = asyncio.create_task(send_email_make_booking(email_address, email_text, email_title, user_name, aud_name, start_time, end_time, pair_number, bb_number, preferences_list))

    res = await asyncio.gather(response)
    return res


def send_email_booking(
        email_address,
        email_text,
        email_title,
        user_name="Александр Сергеевич",
        aud_name="524 ГК",
        start_time="18:35",
        end_time="23:59",
        pair_number="3",
        bb_number=5,
        preferences_list="свежий воздух, тихая музыка"):
    send_email_result = asyncio.run(send_email_prev_booking(email_address, email_text, email_title, user_name, aud_name, start_time, end_time, pair_number,bb_number, preferences_list))
    return send_email_result


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

    data = {
            "email_key": EMAIL_KEY,
            "type":"send_text_email",
            "email_address":email_address,
            "email_text":email_text,
            "email_title": email_title
        }

    response = session.post(
        web_address + ":8083/send_email/",
        data=data,
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Email отправлен. A:{email_address}, T:{email_title} data={data}", "i")

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


def get_bb_amount_by_email(email=""):
    log(f"============={email}", "i")
    if "phystech.edu" in email:
        return 28
    return 0


def create_user_wallet(username, token="", email=""):
    log(f"Начало создания кошелька пользователя. U:{username}, T{token}", "d")
    if len(UsersWallet.objects.filter(username=username)) != 0:
        log(f"При создании кошелька пользователь не был найден. U:{username}", "e")
        return False
    users_wallet = UsersWallet(
        username=username,
        email=email,
        token=token,
        number_bb=get_bb_amount_by_email(email)
    )
    users_wallet.save()
    log(f"Кошелёк пользователя успешно создан. U:{username}", "d")
    return users_wallet


def update_user_wallet(username, token="", email=""):
    log(f"Начало создания кошелька пользователя. U:{username}, T{token}", "d")
    user_len = len(UsersWallet.objects.filter(email=email))
    if user_len > 1:
        log(f"При создании кошелька пользователь не был найден. U:{username}", "e")
        return False
    elif user_len == 1:
        users_wallet = UsersWallet.objects.get(email=email)
        users_wallet.username = username
        users_wallet.token = token
        users_wallet.save()
        log(f"Кошелёк пользователя успешно обновлён. U:{username}", "d")
    elif user_len == 0:
        users_wallet = UsersWallet(
                username=username,
                email=email,
                token=token,
                number_bb=get_bb_amount_by_email(email))
        users_wallet.save()
        log(f"Кошелёк пользователя успешно создан и обновлён. U:{username}", "d")
    return users_wallet


def mark_not_my_booking(user, booking):
    """ Добавляем ответ на сообщение пользователя о занятости """
    log(f"Начло маркировки о занятости: mark_not_my_booking", "i")
    if len(get_mark_busy_array(user)) > 5:
        log(f"Маркировка недобросовестным пользователем: {user.username}", "i")
        # В случае множественных сообщений обнуляем рейтинг доверия пользователя

        setup_user_trust_rate(user, 0)
    if validate_booking(booking):
        mark = MarkedBusy(
            user=user,
            audience=booking.audience,
            trust_rate=user.trust_rate
        )
        log(f"Запрос на занятость аудитории получен: "
            f"user={user.username} booking={booking.audience.number}", "i")
        mark.save()
        # Пересчитываем рейтинг доверия к пользователю
        recalculate_trust_rate(user)
        # Обновляем оценки загруженности в соответствии с доверием
        update_busy_marks()
        # Выдаём пользователю новую аудиторию
        update_reserved_audience(booking)


def mark_this_is_my_booking(user, booking):
    """ Добавляем ответ на сообщение пользователя о занятости """
    if validate_booking(booking):
        mark = MarkedBooked(
            user=user,
            audience=booking.audience,
            trust_rate=user.trust_rate
        )
        mark.save()

        # Устанавливаем занятость аудиторий
        audience = Audience.objects.get(id=booking.audience.id)
        audience.audience_status = AudienceStatus.objacts.get(name="Занято")
        audience.audience_status.save()
        audience.save()

        log("Запрос на нахождение в аудитории получен: "
            "user={user.username} booking={booking.audience.number}", "i")
        # Пересчитываем рейтинг доверия к пользователю
        recalculate_trust_rate(user)
        # Обновляем оценки загруженности в соответствии с доверием
        update_busy_marks()


def update_reserved_audience(booking):
    log(f"Обновление зарезервированных аудиторий: booking={booking.audience.number}", "i")
    free_audiences = \
        Audience.objects.filter(
            audience_status__name="Резерв")
    log(f"Число аудиторий для замены: {len(free_audiences)}", "i")
    if len(free_audiences) != 0:
        log(f"Новая аудитория: number={free_audiences[0].number}", "i")
        booking.audience = free_audiences[0]
        booking.audience.save()
        booking.save()


def get_mark_busy_array(user):
    """ Получаем все занятые аудитории за сегодня """
    yesterday = timezone.now() - timedelta(days=1)
    mark_busy_array = MarkedBusy.objects.filter(
        user=user,
        mark_time__gte=yesterday)
    return mark_busy_array


def setup_user_trust_rate(user, trust_rate):
    """ Устанавливаем рейтинг доверия пользователю """
    user = UsersWallet.objects.get(username=user.username)
    user.trust_rate = trust_rate
    user.save()


def recalculate_trust_rate(user):
    """ Функция для пересчёта рейтинга доверия к пользователю """
    # Берём все бронирования за последние сутки
    mark_busy_array = get_mark_busy_array(user)
    log(f"Пересчёт рейтинга доверия: "
        f"user={user.username}", "i")

    # Устанавливаем рейтинг бронирования за последние сути на 1
    # Даем пользователю кредит доверия на сегодня
    final_rate = 1
    for index,mark in enumerate(mark_busy_array):
        if index != 0:
            log(f"{index}", "")
            # Считаем временной зазор в секундах
            time_gap = int(mark.mark_time.strftime('%s')) - int(mark_busy_array[index - 1].mark_time.strftime('%s'))
            # Обрабатываем случай двойного клика
            final_rate *= min(30, time_gap)/30
    setup_user_trust_rate(user, final_rate)

    log(f"FINAL TRUST RATE: tr={final_rate} username={user.username}", "i")
    return final_rate


def update_busy_marks():
    # Обновляем оценки по занятости аудиторий
    log(f"Обновление занятых аудиторий", "i")
    audiences = Audience.objects.all()
    for audience in audiences:
        busy_rate = 0
        # Определяем временной промежуток в один час для корректности
        last_hour = timezone.now() - timedelta(hours=1)
        # Выбираем те упоминания которые могут соответствовать, т.е. час
        for busy_mark in MarkedBusy.objects.filter(
                audience=audience,
                mark_time__gte=last_hour):
            busy_rate += busy_mark.trust_rate
        # При превышении суммарного рейтинга доверия числа - срабатывает
        # Делаем аналог кросс-валидации
        if busy_rate != 0:
            log(f"Обновление статуса: number={audience.number} busy_rate={busy_rate} busy_barrier={0.5}", "i")
            if busy_rate > 0.5:
                audience.audience_status = AudienceStatus.objects.get(name="Занято")
                audience.audience_status.save()
                audience.save()
                # Удаляем упоминания о занятости аудиторий
                MarkedBusy.objects.filter(audience=audience).delete()


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


def get_time_slots(audience_number):
    log(f"Получение расписания бронирования.", "d")
    res = []
    audiences = Audience.objects.filter(number=audience_number)
    for item in audiences:
        val = {
            "status": item.audience_status.name,
            "day_history": item.day_history.pair,
            "date": item.day_history.date
        }
        res.append(val)
    return res


def get_week_time_slots(audience_number):
    log(f"Получение расписания бронирования.", "d")
    res = []
    audiences = Audience.objects.filter(number=audience_number)
    for item in audiences:
        val = {
            "status": item.audience_status.name,
            "day_history": item.week_pairs
        }
        res.append(val)
    return res


def get_book_audience_response(
        number: str,
        user: str,
        email: str,
        number_bb: int,
        pair_number: int,
        time_slot: int):
    log(f"BOOK_AUDIENCE number={number} user={user} email={email} number_bb={number_bb} pair_number={pair_number} time_slot={time_slot}", "i")
    
    if len(Book.objects.filter(user=get_user_by_username(user))) > 0:
        log(f"Бронирование пользователя уже существует: u={user} number={number}", "i")
        return Response(
            {
                "result": False,
                "Error": f"Бронирование пользователя уже существует: u={user} number={number}" 
            },
            status=status.HTTP_204_NO_CONTENT)

    if get_audience_by_number(number) is None:
        log(f"Аудитория отсутствует: u={user} number={number}", "i")
        return Response(
            {
                "result": False,
                "Error": f"Аудитории не существует: u={user} number={number}"
            },
            status=status.HTTP_204_NO_CONTENT)

    if get_user_by_username(user) is None:
        log(f"Пользователь отсутствует: u={user} number={number}", "i")
        return Response(
            {
                "result": False,
                "Error": f"Пользователя не существует: u={user} number={number}"
            },
            status=status.HTTP_204_NO_CONTENT)
    
    new_book = Book(
        audience=get_audience_by_number(number),
        user=get_user_by_username(user),
        number_bb=number_bb,
        pair_number=pair_number,
        time_slot=time_slot,
        date=datetime.datetime.now().date(),
        booking_time=datetime.datetime.now().time(),
        visibility=1)
    new_book.save()
    log(f"++++++{number}", "i")
    audience = Audience.objects.get(number=number)
    if audience.day_history.pair[pair_number][1] == "Свободно":
        # Останавливаем мгновенные бронирования
        ## audience.day_history.pair[pair_number][1] = "Занято"

        for i in range(pair_number):
            if (time_slot+i) < len(audience.day_history.pair):
                log(f"===== Отметка о брониа аудитории: ts={time_slot+i} number={number}", "i")
                audience.day_history.pair[time_slot+i][1] = "Забронировано"
        audience.day_history.save()
        audience.save()

        log(f"Изменена дневная история. A:{number}, P:{pair_number}", "d")
        ## audience.day_history.pair[pair_number][2] = user
        log(f"Изменён пользователь дневной истории. A:{number}, U:{user}", "d")
        ## audience.day_history.pair[pair_number][3] = str(number_bb)
        log(f"Изменены баллы бронирования дневной истории. A:{number}, BB:{number_bb}", "d")
        ## audience.audience_status = AudienceStatus.objects.get(name="Занято")
        ## audience.audience_status.save()
        log(f"Статус занятости сохранён. A:{number}", "d")
        ## audience.day_history.save()
        log(f"Дневная история сохранена. A:{number}", "d")
        ## audience.save()
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
        # send_email(email_address, email_text, email_title)
        log(f"TSA={TIME_SLOT_ARR} pn={pair_number} ts={time_slot}", "i")
        send_email_booking(
            email_address,
            email_text,
            email_title,
            user_name=f"{new_book.user.username}",
            aud_name=number,
            start_time=TIME_SLOT_DICT[time_slot],
            end_time=TIME_SLOT_DICT[min(time_slot+pair_number, 13)],
            pair_number=pair_number,
            bb_number=number_bb,
            preferences_list="тепло, хорошо"
        )

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
        case _:
            logging.debug(_)


# BOOKING ITERATION

def get_queue_item(booking) -> dict:
    # Формируем единицу очереди на основе заявки на бронирование
    log(f"UPDATE: get_queue_item", "i")
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
    # Проверяем временную возможность бронирования на заданный временной слот
    log(f"CHECK BOOKING AVAIL:"
        f" b_ts={booking.time_slot} ts={time_slot} b_pn={booking.pair_number}", "i")
    if booking.time_slot <= time_slot < booking.time_slot + booking.pair_number:
        # Если бронирование вместе с количеством пар раньше по времени, чем
        # текущий временной слот, что бронирование удаляется (переноситься в историю)
        return True
    else:
        # Удаляем устаревшие бронирования
        if booking.time_slot + booking.pair_number <= time_slot:
            booking.to_history()
    return False


def make_queue_list(time_slot: int):
    # Создаем очередь бронирования на основе текущего временного слота
    log(f"UPDATE: make_queue_list", "i")
    all_booking = Book.objects.all()
    result_queue = []
    # TODO: сделать проверку на наличие двойного бронирования аудитории
    # Сейчас делается предположение что бронирование возможно только одной аудитории
    for booking in all_booking:
        if check_booking_availability(booking, time_slot):
            # В случае успешной проверки на время бронирование добавляется в очередь
            result_queue.append(get_queue_item(booking))
    return result_queue


def time_slot_to_time(slot_number):
    # переводим номер временного слота в текстовое время
    log(f"UPDATE: time_slot_to_time", "i")
    slot_dict = TIME_SLOT_DICT
    return slot_dict[slot_number]


def get_confirmation_text(queue_item, username):
    # Текст письма с подтверждением успешного бронирования аудитории
    log(f"UPDATE: get_confirmation_text", "i")
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
    # Текст письма с уведомлением о невозможности бронирования
    log(f"UPDATE: get_reject_text", "i")
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
    # Текст письма с уведомлением о завершении бронирования
    log(f"UPDATE: get_end_booking", "i")
    return f"Уважаемый, {username}\n\n" \
           f"Сообщаем Вам, что бронирование аудитории {audience_number} завершено. " \
           f"Просьба покинуть аудиторию или забронировать следующую\n" \
           f"\n\tНомер аудитории: {audience_number}\n" \
           f"\tВремя бронирования: {time_slot_to_time(time_slot)}\n" \
           f"\tОбщая продолжительность: {pair_number}\n" \
           f"\tСписанные баллы бронирования: {number_bb} ББ {ADMIN_FOOTER_INFO}"


def check_queue_list(time_slot: int):
    # Создание очереди бронирования и возвращения списка сообщений и аудиторий
    # Число доступных для бронирования аудиторий (может меняться)
    log(f"UPDATE: check_queue_list", "i")
    number_of_audiences = len(Audience.objects.exclude(audience_status__name='Отсутствует для бронирования'))
    queue_list = make_queue_list(time_slot)
    queue = sorted(queue_list, key=lambda item: int(item["number_bb"]), reverse=True)

    for queue_item in queue:
        queue_item["user_wallet"].number_bb = max(int(queue_item["user_wallet"].number_bb) - int(queue_item["number_bb"]), 0)

    email_list = make_email_list(queue, number_of_audiences)
    audience_list = make_audience_list(queue, number_of_audiences)

    return email_list, audience_list


def make_audience_list(queue, number_of_audiences):
    log(f"UPDATE: make_audience_list", "i")
    # Создание списка аудиторий по очереди бронирования и числу доступных аудиторий
    for i in range(max(number_of_audiences, len(queue))):
        log(f"UPDATE: make_audience_list | index:{i}", "i")
        if i < min(number_of_audiences, len(queue)):
            log(f"UPDATE: make_audience_list | Принято", "i")
            queue[i]["status"] = "Принято"
        elif i < len(queue):
            log(f"UPDATE: make_audience_list | Отклонено", "i")
            queue[i]["status"] = "Отклонено"

    audience_list = []
    for queue_item in queue:
        if queue_item["status"] == "Принято":
            audience_list.append(queue_item)

    return audience_list


def make_email_list(queue, number_of_audiences):
    log(f"UPDATE: make_email_list", "i")
    # Создание списка рассылки уведомлений о бронировании
    email_list = []
    for i in range(max(number_of_audiences, len(queue))):
        log(f"UPDATE: make_email_list | index:{i}", "i")
        if i < min(number_of_audiences, len(queue)):
            log(f"UPDATE: make_email_list | Бронирование прошло успешно", "i")
            email_list.append({
                "email": queue[i]['user_wallet'].email,
                "title": f"Бронирование прошло успешно | {queue[i]['audience'].number}",
                "text": get_confirmation_text(
                    queue_item=queue[i],
                    username=queue[i]['user_wallet'].username)})
        elif i < len(queue):
            log(f"UPDATE: make_email_list | Бронирование не удалось", "i")
            email_list.append({
                "email": queue[i]['user_wallet'].email,
                "title": f"Бронирование не удалось | {queue[i]['audience'].number}",
                "text": get_reject_text(
                    queue_item=queue[i],
                    username=queue[i]['user_wallet'].username,
                    queue_number=i,
                    queue_len=len(queue),
                    places_number=number_of_audiences,
                    min_bb_number=queue[min(number_of_audiences, len(queue)-1)]["number_bb"]
                )})
    return email_list


def update_audience_day(week_day):
    for audience in Audience.objects.all():
        log(f"============ WEEK_DAY={week_day}"
            f" LEN={len(audience.week_pairs)}"
            f" AN={audience.number}", "i")
        if week_day < 6:
            # Обновляем понедельник - субботу
            audience.day_history.pair = audience.week_pairs[week_day]
            log(f"99999999999 {audience.week_pairs[week_day]}", "i")
        elif week_day == 6:
            # Обновляем воскресенье через очищение
            audience.make_all_free()
        audience.day_history.save()
        audience.save()


def create_reserve(building_name="ГК"):
    free_audiences = Audience.objects.filter(audience_status__name="Свободно",
                                             building__name=building_name)
    for index,audience in enumerate(free_audiences):
        if index < len(free_audiences)/3:
            log(f"RESERVE: update_audience | number:{str(audience.number)}", "i")
            audience.audience_status = AudienceStatus.objects.get(name="Резерв")
            audience.audience_status.save()
            audience.save()


def update_audience(time_slot: int):
    log(f"UPDATE: update_audience", "i")
    # получаем список почт и аудиторий сделанный после проверки и создания очереди
    email_list, audience_list = check_queue_list(time_slot)
    log(f"UPDATE: update_audience | email_list:{str(email_list)}, audience_list:{str(audience_list)}", "i")

    # Очищаем бронирования, обновляем статусы и загружаем бронирования из расписания
    clear_audience(time_slot)

    # Загружаем бронирования в список на сайте
    load_booking(audience_list)

    # Создаём резервирования аудиторий для ошибочной занятости
    create_reserve()

    # Обновление email и их окончательная отправка
    new_email_list = update_email_list_by_stop_booking(email_list, audience_list, time_slot)
    log(f"UPDATE: update_audience | new_email_list:{str(new_email_list)}", "i")
    for email in new_email_list:
        log(f"UPDATE: update_audience | email:{str(email)}", "i")
        send_email(
            email_address=email["email"],
            email_text=email["text"],
            email_title=email["title"])


def clear_audience(time_slot: int):
    log(f"UPDATE: clear_audience", "i")
    # Очистка бронирований на текущий временной слот
    ## audiences = Audience.objects.exclude(audience_status__name='Отсутствует для бронирования')
    # Очищаем бронирования всех аудиторий
    audiences = Audience.objects.all()
    for audience in audiences:
        log(f"UPDATE: clear_audience | number={audience.number} | ts={time_slot - 1} | make free", "i")
        # Очищаем бронирования, обновляем статусы и загружаем бронирования из расписания
        audience.clear_booking(time_slot - 1)
        audience.save()


def load_booking(audience_list):
    log(f"UPDATE: load_booking", "i")
    # Загрузка списка аудиторий для отображения статусов
    # TODO: сделать обновление дневной истории бронирования
    # TODO: сделать "скоро освободиться"
    for audience in audience_list:
        log(f"UPDATE: load_booking | number:{audience['audience'].number}", "i")
        if len(Audience.objects.filter(number=audience['audience'].number)) == 1:
            log(f"UPDATE: load_booking | number:{audience['audience'].number} | make closed", "i")
            this_audience = Audience.objects.get(number=audience['audience'].number)
            this_audience.audience_status = AudienceStatus.objects.get(name="Занято")
            this_audience.audience_status.save()
            this_audience.save()
        else:
            log(f"Error: wrong loading audience: {audience['audience'].number}", "i")


def update_email_list_by_stop_booking(email_list, audience_list, time_slot):
    log(f"UPDATE: update_email_list_by_stop_booking", "i")
    # добавление списка почты уведомлениями о завершении бронирования
    audiences = Audience.objects.all()
    for audience in audiences:
        log(f"UPDATE: update_email_list_by_stop_booking | number:{audience.number}", "i")
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


def validate_booking(booking):
    """ Запрос на корректность бронирования и уведомления от пользователя """
    time_slot = get_time_slot()
    if booking.time_slot <= time_slot < booking.time_slot + booking.pair_number:
        log(f"Корректность подтверждена: number={booking.audience.number}", "i")
        return True
    log(f"Заявка от пользователя не корректна: "
        f"number={booking.audience.number} "
        f"time_slot={time_slot} "
        f"booking.time_slot={booking.time_slot} "
        f"booking.time_slot + booking.pair_number={booking.time_slot + booking.pair_number}", "i")
    return True
    # return False


def get_time(time_string):
    return datetime.datetime.strptime(time_string, "%H:%M")


def get_time_slot():
    CurrentPair = namedtuple('CurrentPair', ['number', 'start_time', 'end_time'])
    current_pair_list = [
        CurrentPair(1, "09:00", "10:25"),
        CurrentPair(2, "10:25", "12:10"),
        CurrentPair(3, "12:10", "13:55"),
        CurrentPair(4, "13:55", "15:30"),
        CurrentPair(5, "15:30", "17:05"),
        CurrentPair(6, "17:05", "18:30"),
        CurrentPair(7, "18:30", "20:00"),
        CurrentPair(8, "20:00", "22:00"),
        CurrentPair(9, "22:00", "23:59"),
        CurrentPair(10, "00:00", "01:30"),
        CurrentPair(11, "01:30", "03:00"),
        CurrentPair(12, "03:00", "04:30"),
        CurrentPair(13, "04:30", "06:00")]
    now = datetime.datetime.now()

    for current_pair in current_pair_list:
        if get_time(current_pair.start_time).time() < now.time() < get_time(current_pair.end_time).time():
            return current_pair.number
    return -1
