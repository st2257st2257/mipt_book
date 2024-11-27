import django.contrib.postgres.fields
from django.db import migrations, models
import pandas as pd
import os
import re
import datetime
# Код позволяет получить последнее время занятия аудиторий
# по заданному файлу расписания
# (c) Aleksandr Kristal @st2257

import pandas as pd
import numpy as np
from main.services import log
from collections import namedtuple

building_arr = ['ГК', 'ЛК', 'Акт.зал', 'КПМ', 'Гл.Физ.', 'Цифра', 'Квант', 'УПМ', 'ауд.', 'ОКТЧ', 'БК', 'Арктика']

PAIR_INDEX_DICT = {
    "9:00 - 10:25": 0,
    "10:45 - 12:10": 1,
    "12:20 - 13:45": 2,
    "13:55 - 15:20": 3,
    "15:30 - 16:55": 4,
    "17:05 - 18:30": 5,
    "18:35 - 20:00": 6,
    "20:00 - 22:00": 7
}

DAYS_INDEX_DICT = {
    "Понедельник": 0,
    "Вторник": 1,
    "Среда": 2,
    "Четверг": 3,
    "Пятница": 4,
    "Суббота": 5,
    "Воскресенье": 6}

TIME_SLOT_DICT = {
    1: "09:00",
    2: "10:45",
    3: "12:20",
    4: "13:45",
    5: "15:30",
    6: "17:05",
    7: "18:35",
    8: "20:00",
    9: "22:00",
    10: "23:59",
    11: "01:30",
    12: "03:00",
    13: "04:30",
    14: "06:00",}

WEEK_DAYS_DICT = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье",}


def get_building(string_pair_number):
    # определяем все доступные здания
    for building in building_arr:
        if building in string_pair_number:
            return building
    return None


def get_audience_by_pair_name(pair_name):
    char_len = 0  # длина названия здания
    digit_number = 0  # число цифр в названии
    start_index = 0  # начальный индекс номера аудитории
    for (i, char) in enumerate(pair_name):
        # считаем длину названия аудитории
        if str(char).isdigit() or ((char == '.' or char == '0') and char_len != 0):
            char_len += 1
        if str(char).isdigit():
            digit_number += 1

        if char_len == 1:
            start_index = i
        # выводим итоговые номер аудитории и название здания
        if not str(char).isdigit() and char != '.':
            if char_len > 2 and digit_number != 4:
                return (
                    pair_name[start_index:start_index + char_len],  # number
                    get_building(pair_name)  # building
                )
            elif char_len == 4:
                return (
                    pair_name[start_index:start_index + char_len],  # number
                    'ауд.'  # building
                )
            else:
                char_len = 0
                start_index = 0
    return None


def print_data(file_name, sheet_name):
    data = pd.read_excel(file_name, sheet_name=sheet_name)

    res = []

    for i in range(len(data.values)):
        res.append(data.values[i])
        print(data.values[i])
    return res


def get_event_list(file_name, sheet_name):
    res_data = print_data(file_name, sheet_name)
    res_array = []
    for (index, string) in enumerate(res_data[0]):
        for j in range(len(res_data)):
            aud_name = get_audience_by_pair_name(str(string))
            pair_name = str(res_data[j][index])
            if res_data[j][1] in PAIR_INDEX_DICT.keys() and res_data[j][0] in DAYS_INDEX_DICT.keys() and pair_name != "nan":
                pair_index = PAIR_INDEX_DICT[res_data[j][1]]
                day_index = DAYS_INDEX_DICT[res_data[j][0]]
                res_array.append((aud_name, day_index, pair_index, pair_name))
    return res_array


def remove_phone_numbers(text):
    phone_pattern = r"(?:\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    cleaned_text = re.sub(phone_pattern, "", text)
    return cleaned_text


def read_excel_timetable(apps, schema_editor):
    """Заполняет таблицу базовыми значениями, забитыми в эксель файле"""
    """Заполняется: Аудитории, Кошельки"""

    # Создаем аудитории для бронирования
    Building = apps.get_model('main', 'Building')
    AudienceStatus = apps.get_model('main', 'AudienceStatus')
    Audience = apps.get_model('main', 'Audience')
    DayHistory = apps.get_model('main', 'DayHistory')

    # Создаем мероприятия для поиска по ним
    EventItem = apps.get_model('events', 'EventItem')
    EventType = apps.get_model('events', 'EventType')
    Pair = apps.get_model('events', 'Pair')

    # Читаем данные файлов и записываем их в соответствующий класс
    audience_event_list = get_event_list("excel/res_aud.xlsx", "Лист1")

    # Building.objects.all().delete()
    # AudienceStatus.objects.all().delete()
    Audience.objects.all().delete()
    DayHistory.objects.all().delete()
    aud_ev_len = len(audience_event_list)

    # Получаем дефолтные значения
    audience_status = AudienceStatus.objects.get(name="Свободно")
    event_type = EventType.objects.get(name="Лекция")

    for index, audience_event in enumerate(audience_event_list):
        log(f"{index}/{aud_ev_len}", "d")
        audience_number = ""
        building_name = ""
        try:
            audience_number = audience_event[0][0]
            building_name = audience_event[0][1]
        except Exception as e:
            log(e, 'e')
            continue
        day_index = audience_event[1]
        pair_index = audience_event[2]
        pair_name = audience_event[3]

        # Создаем мероприятие
        name = pair_name
        description = pair_name
        EventItem.objects.filter(name="Лекция").delete()
        if len(Pair.objects.filter(time_slot_index=pair_index+1, week_day_index=day_index+1)) == 1 and \
                len(EventType.objects.filter(name="Лекция")) == 1:
            # Создаем и добавляем событие
            pair = Pair.objects.get(time_slot_index=pair_index+1, week_day_index=day_index+1)

            # Удаляем те же самые события
            EventItem.objects.filter(name=name[:63],pair=pair).delete()

            event_item = EventItem.objects.create(
                name=remove_phone_numbers(name[:63]),
                description=remove_phone_numbers(description[:254]),
                pair=pair,
                owner_user_wallet="mipt",
                event_type=event_type,
                audience_number=f"{audience_number} {building_name}"
            )
            event_item.save()

        audience_list = Audience.objects.filter(number=audience_number)
        building_list = Building.objects.filter(name=building_name)

        if len(building_list) == 1:
            build = building_list[0]
            if len(audience_list) == 0:
                _audience = Audience.objects.create(
                    number=audience_number,
                    description=f"Аудитория номер: {audience_number} {building_name}",
                    building=build,
                    audience_status=audience_status,
                    number_of_users=20,
                    day_history=DayHistory.objects.create(
                        pair=[
                            [
                                TIME_SLOT_DICT[i+1],   #  время бронирования
                                "Свободно",            #  статус аудитории
                                "blank_user",          #  кто бронирует аудиторию
                                "0",                   #  число баллов бронирования
                                "20",                  #  число человек, которое вмещает аудитория
                                "",
                                ""
                            ] for i in range(14)],
                        date="2024-01-01"),
                    week_pairs=[
                        [
                            [
                                TIME_SLOT_DICT[i+1], #  время бронирования
                                "Свободно",          #  статус аудитории
                                "Отсутствует",       #  кто бронирует аудиторию
                                "0",                 #  число баллов бронирования
                                "20",                #  число человек, которое вмещает аудитория
                                WEEK_DAYS_DICT[j],   #  день недели
                                "",                  #  название мероприятия
                            ]
                        for i in range(14)] for j in range(1,8)])
                _audience.day_history.audience = _audience
                _audience.day_history.save()
            if len(audience_list) == 1:
                _audience = audience_list[0]
                _audience.week_pairs[day_index][pair_index][1] = "Отсутствует для бронирования"
                if len(pair_name) > 6:
                    if pair_name[3] == "-" and (pair_name[3] == "М" or pair_name[3] == "Б"):
                        _audience.week_pairs[day_index][pair_index][2] = pair_name[0:6]
                    else:
                        _audience.week_pairs[day_index][pair_index][2] = "Лекция"
                _audience.week_pairs[day_index][pair_index][6] = remove_phone_numbers(pair_name)
                _audience.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0014_markedbooked'),
    ]

    operations = [
        migrations.RunPython(read_excel_timetable),
    ]
