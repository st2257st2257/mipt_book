# email text configurations
CHANGE_NAME_TITLE = "Изменение ФИО пользователя"
ADMIN_FOOTER_INFO = "\n\nС уважением,\n" \
                    "Сервис бронирования аудиторий МФТИ\n" \
                    "info@mipt.site\n" \
                    "https://mipt.site"


def get_booking_text(username, pair_number, audience, number_bb):
    final_string = f"Уважаемый, {username},\n\n" \
                   f"Вы забронировали аудиторию на сайте бронирования аудиторий МФТИ https://mipt.site\n\n" \
                   f"Параметры бронирования:\n" \
                   f"Номер аудитории: {audience}\n" \
                   f"Номер пары бронирования: {pair_number}\n" \
                   f"Число списанных баллов бронирования: {number_bb}" \
                   f"{ADMIN_FOOTER_INFO}"
    return final_string


def get_stop_booking_text(username, audience_number):
    final_string = f"Уважаемый, {username},\n\n" \
                   f"Вы отменили бронирование аудитории {audience_number}ГК" \
                   f"{ADMIN_FOOTER_INFO}"
    return final_string
