import django.contrib.postgres.fields
from django.db import migrations, models
import pandas as pd
import os
import datetime
# Код позволяет получить последнее время занятия аудиторий
# по заданному файлу расписания
# (c) Aleksandr Kristal @st2257

import pandas as pd
import numpy as np
from main.services import log
from collections import namedtuple


PAIR_NAME_ARR = {
    '900 - 1025': 1,
    '1045 - 1210': 2,
    '1220 - 1345': 3,
    '1355 - 1520': 4,
    '1530 - 1655': 5,
    '1705 - 1830': 6,
    '1835 - 2000': 7}

PAIR_NAME_DICT = {
    1: '900 - 1025',
    2: '1045 - 1210',
    3: '1220 - 1345',
    4: '1355 - 1520',
    5: '1530 - 1655',
    6: '1705 - 1830',
    7: '1835 - 2000'}

building_arr = ['ГК', 'ЛК', 'Акт.зал', 'КПМ', 'Гл.Физ.', 'Цифра', 'Квант', 'УПМ', 'ауд.', 'ОКТЧ', 'БК', 'Арктика']

week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']


class Timetable:
    def __init__(self, year_number=""):
        self.year_number = year_number
        self.group_arr = []

    def append(self, group):
        self.group_arr.append(group)

    def get_group_by_name(self, group_name):
        for group in self.group_arr:
            if group.name == group_name:
                return group
        return None

    def get_group_pair_name(self, group_name, week_day, pair_number):
        for group in self.group_arr:
            if group.name == group_name:
                return group.get_pair_name(week_day, pair_number)
        return None


class Group:
    def __init__(self, name):
        self.name = name
        self.event_arr = []

    def __str__(self):
        string = ""
        for event in self.event_arr:
            string += f"name: {self.name} event: {event}\n"
        return string

    def __del__(self):
        self.name = ""
        self.event_arr = []

    def clear(self):
        self.event_arr = []

    def append(self, event):
        self.event_arr.append(event)

    def get_pair_name(self, week_day, pair_number):
        for event in self.event_arr:
            if event.week_day == week_day and event.pair_number == pair_number:
                return event.pair_name
        return ""


class EventItem:
    # week_day = ''  # ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')
    # day_time = ''  # ('900 - 1025', '1045 - 1210', '1220 - 1345', '1355 - 1520', '1530 - 1655', '1705 - 1830', '1835 - 2000')
    # pair_name = ''
    # pair_number = 0

    def __init__(self, week_day, day_pair, pair_name):
        self.week_day = week_day
        self.day_time = day_pair
        self.pair_name = pair_name
        self.pair_number = 0
        self.audience_number = ""
        self.building_name = ""

    def __str__(self):
        return f"DT:{self.day_time} WD:{self.week_day} DT:{self.day_time} PN:{self.pair_name} PNb:{self.pair_number}"

    def update_pair_number(self):
        if self.day_time in PAIR_NAME_ARR.keys():
            self.pair_number = PAIR_NAME_ARR[self.day_time]
            return True
        return False


class Pair:
    def __init__(self, day_time='', pair_name='', audience_number='', building='', group_name=''):
        self.audience_number = audience_number
        self.building = building
        self.pair_name = pair_name
        self.day_time = day_time
        self.group_name = group_name

    def __str__(self):
        return f"PAIR - " \
               f"AN:{self.audience_number} " \
               f"B:{self.building} " \
               f"PN:{self.pair_name} " \
               f"DT:{self.day_time} " \
               f"GN: {self.group_name}"


class DayTimetable:
    def __init__(self):
        self.pair_arr = {
            '900 - 1025': Pair(day_time='900 - 1025'),
            '1045 - 1210': Pair(day_time='1045 - 1210'),
            '1220 - 1345': Pair(day_time='1220 - 1345'),
            '1355 - 1520': Pair(day_time='1355 - 1520'),
            '1530 - 1655': Pair(day_time='1530 - 1655'),
            '1705 - 1830': Pair(day_time='1705 - 1830'),
            '1835 - 2000': Pair(day_time='1835 - 2000')}

    def upend(self, pair_name, day_time, group_name=''):
        self.pair_arr[day_time].pair_name = pair_name
        self.pair_arr[day_time].group_name = group_name

    def get_last(self):
        for day_time in list(reversed(self.pair_arr.keys())):
            # print(self.pair_arr[day_time])
            # print(self.pair_arr[day_time].group_name)
            if len(self.pair_arr[day_time].group_name) > 0:
                return self.pair_arr[day_time]
        return self.pair_arr['900 - 1025']

    def __str__(self):
        return f"DayTimetable: '900 - 1025':{self.pair_arr['900 - 1025']} ... "


class WeekTimetable:
    def __init__(self):
        self.day_arr = {
            'Понедельник': DayTimetable(),
            'Вторник': DayTimetable(),
            'Среда': DayTimetable(),
            'Четверг': DayTimetable(),
            'Пятница': DayTimetable(),
            'Суббота': DayTimetable()
        }

    def append(self, week_day, day_time, pair_name, group_name=''):
        if week_day in self.day_arr.keys():
            self.day_arr[week_day].upend(pair_name, day_time, group_name)

    def __str__(self):
        return f"WeekTimetable: Понедельник:{self.day_arr['Понедельник']} ..."


class Audience:
    def __init__(self, number, building):
        self.number = number
        self.building = building
        self.timetable = WeekTimetable()

    def append(self, week_day, day_time, pair_name, group_name=''):
        self.timetable.append(week_day, day_time, pair_name, group_name)

    def get_last_event(self, week_day):
        day = self.timetable.day_arr[week_day]
        last_event = day.get_last()
        return last_event

    def get_name(self):
        return f"{self.number} {self.building}"

    def __str__(self):
        return f"Audience: N:{self.number} B:{self.building} T:{self.timetable}"


class AudienceList:
    def __init__(self):
        self.audience_list = []

    def __add__(self, other):
        audience_list = AudienceList()
        for audience_other in other.audience_list:
            audience_list.audience_list.append(audience_other)
        return self

    def create_new(self, audience_number, audience_building):
        self.audience_list.append(Audience(audience_number, audience_building))

    def add_time_slot(
            self,
            audience_number,
            audience_building,
            week_day,
            day_time,
            pair_name,
            group_name=''):
        for audience in self.audience_list:
            if audience.number == audience_number and audience.building == audience_building:
                audience.append(week_day, day_time, pair_name, group_name)

    def is_in(self, audience_number, building_name):
        for audience in self.audience_list:
            if audience.number == audience_number and audience.building == building_name:
                return True
        return False

    def get_len(self):
        return len(self.audience_list)

    def get_audience(self, audience_number, building_name):
        for audience in self.audience_list:
            # print(audience.number)
            if audience.number == audience_number and audience.building == building_name:
                return audience
        return None

    def __str__(self):
        string = ""
        for audience in self.audience_list:
            string += str(audience) + "\n"
        return string

    def get_last_dict(self):
        res_dict = {}
        for audience in self.audience_list:
            MyAudience = namedtuple('MyAudience', ['aud_number', 'aud_building', 'last_time'])
            days_dict = {}
            my_aud = MyAudience(audience.number, audience.building, '')

            for week_day in week_days:
                days_dict[week_day] = self.get_audience(my_aud.aud_number, my_aud.aud_building).get_last_event(
                    week_day).day_time
            res_dict[audience.get_name()] = days_dict
        return res_dict


def get_pair_number_by_list_index(right_list, list_index):
    # right_list - лист соответствия индекса пары и её номера в классическом исполнении
    # list_index - номер события в таблице
    return right_list[list_index]


def make_timetable(file_name="res_data.xlsx", sheet_name="1 курс"):
    # current_dir = os.getcwd()
    # file_path = os.path.join(current_dir, file_name)
    # data = pd.read_excel(file_path, sheet_name=sheet_name)
    data = pd.read_excel(file_name, sheet_name=sheet_name)
    log(data, "i")

    temp_arr = []
    time_matching_arr = []
    for i in range(len(data.values)):
        cur_array = []
        item = data.values[i]
        for j in range(len(item)):
            cur_array.append(item[j])
        # добавляем считанную строку в массив
        temp_arr.append(cur_array)
        matching_pair = {
            "week_day": cur_array[0],
            "day_pair": cur_array[1]
        }
        time_matching_arr.append(matching_pair)
    # сделали массив соответствия индекса и соответствующего времени

    # формируем список пробелов которые возникают из-за дней и часов
    space_index = []
    space_word_arr = ["Дни", "Часы", 'nan', None]
    for i in range(len(temp_arr[0])):
        if temp_arr[0][i] in space_word_arr:
            space_index.append(i)

    # формируем список групп через транспонирование
    my_matrix = np.array(temp_arr).transpose()

    # создаём массив групп
    timetable = Timetable("Первый курс")
    for i in range(len(my_matrix)):
        # i - индекс группы в заданном списке
        if my_matrix[i][0] not in space_word_arr:  # пропускаем все пустые строчки
            # создаём группу для добавления в финальный массив
            group = Group(name=my_matrix[i][0])
            for j in range(len(my_matrix[i])):
                # j - номер события (пары)
                event_item = EventItem(
                    week_day=time_matching_arr[j]['week_day'],
                    day_pair=time_matching_arr[j]['day_pair'],
                    pair_name=my_matrix[i][j]
                )
                if event_item.update_pair_number() and str(event_item.pair_name) != 'nan':
                    group.append(event_item)
                # print(f"Error in creating group: {event_item}")

            # теперь заполняем массив значениями
            timetable.append(group)

    return timetable


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


def get_audiences(timetable):
    # создаём список аудиторий для заполнения по расписанию
    audience_list = AudienceList()
    # считываем расписания всех групп
    for group in timetable.group_arr:
        # считываем все мероприятия выбранной группы
        for event in group.event_arr:
            # в случае отсутствия аудитории с заданными номером и зданием добавляем её в список
            number, building = "", ""
            if get_audience_by_pair_name(group.get_pair_name(event.week_day, event.pair_number)):
                number, building = get_audience_by_pair_name(group.get_pair_name(event.week_day, event.pair_number))
            if not audience_list.is_in(number, building):
                audience_list.create_new(number, building)

            # добавляем выбранное событие
            audience_list.add_time_slot(
                audience_number=number,
                audience_building=building,
                week_day=event.week_day,
                day_time=event.day_time,
                pair_name=event.pair_name,
                group_name=group.name
            )
    return audience_list


def get_audiences_many(timetables):
    # создаём список аудиторий для заполнения по расписанию
    audience_list = AudienceList()
    # считываем расписания всех групп
    for timetable in timetables:
        for group in timetable.group_arr:
            # считываем все мероприятия выбранной группы
            for event in group.event_arr:
                # в случае отсутствия аудитории с заданными номером и зданием добавляем её в список
                number, building = "", ""
                if get_audience_by_pair_name(group.get_pair_name(event.week_day, event.pair_number)):
                    number, building = get_audience_by_pair_name(group.get_pair_name(event.week_day, event.pair_number))
                if not audience_list.is_in(number, building):
                    audience_list.create_new(number, building)

                # добавляем выбранное событие
                audience_list.add_time_slot(
                    audience_number=number,
                    audience_building=building,
                    week_day=event.week_day,
                    day_time=event.day_time,
                    pair_name=event.pair_name,
                    group_name=group.name
                )
    return audience_list

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


def get_status_by_event_name(audience, i, j):
    if i < 7:
        event_name = audience.timetable.day_arr[WEEK_DAYS_DICT[j]].pair_arr[PAIR_NAME_DICT[i+1]].pair_name
        if event_name == '':
            return 'Свободно'
        return 'Отсутствует для бронирования'
    return 'Свободно'


def get_owner_by_event_group_name(audience, i, j):
    if i < 7:
        group_name = audience.timetable.day_arr[WEEK_DAYS_DICT[j]].pair_arr[PAIR_NAME_DICT[i+1]].group_name
        if group_name == '':
            return 'Отсутствует'
        return group_name
    return 'Отсутствует'


def get_pair_name(audience, i, j):
    if i < 7:
        return audience.timetable.day_arr[WEEK_DAYS_DICT[j]].pair_arr[PAIR_NAME_DICT[i+1]].pair_name
    return ''


def read_excel_timetable(apps, schema_editor):
    """Заполняет таблицу базовыми значениями, забитыми в эксель файле"""
    """Заполняется: Аудитории, Кошельки"""

    # Создаем аудитории для бронирования
    Building = apps.get_model('main', 'Building')
    AudienceStatus = apps.get_model('main', 'AudienceStatus')
    Audience = apps.get_model('main', 'Audience')
    DayHistory = apps.get_model('main', 'DayHistory')

    # Читаем данные файлов и записываем их в соответствующий класс
    # users_wallets = pd.read_excel("excel/res_data1.xlsx", sheet_name="1 курс")
    timetables = [make_timetable(file_name=f"excel/res_data{i}.xlsx", sheet_name=f"{i} курс") for i in range(1, 6)]
    # audiences = [get_audiences(timetables[j]) for j in range(5)]

    # Создаём список последних бронирований
    audience_list = get_audiences_many(timetables)
    # audience_list.audience_list - список всех аудиторий в расписании

    # Building.objects.all().delete()
    # AudienceStatus.objects.all().delete()
    Audience.objects.all().delete()
    DayHistory.objects.all().delete()
    for audience in audience_list.audience_list:
        audience_number = audience.number
        building_name = audience.building

        if len(Building.objects.filter(name=building_name)) == 1:
            build = Building.objects.get(name=building_name)
            audience_status = AudienceStatus.objects.get(name="Свободно")
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
                            "21",                  #  число человек, которое вмещает аудитория
                            "",
                            ""
                        ] for i in range(14)],
                    date="2023-03-08"),
                week_pairs=[
                    [
                        [
                            TIME_SLOT_DICT[i+1],                            #  время бронирования
                            get_status_by_event_name(audience, i, j),       #  статус аудитории
                            get_owner_by_event_group_name(audience, i, j),  #  кто бронирует аудиторию
                            "0",                                            #  число баллов бронирования
                            "20",                                           #  число человек, которое вмещает аудитория
                            WEEK_DAYS_DICT[j],                              #  день недели
                            get_pair_name(audience, i, j),                  #  название мероприятия
                        ]
                    for i in range(14)] for j in range(1,6)])
            _audience.day_history.audience = _audience
            _audience.day_history.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0009_audience_week_pairs'),
    ]

    operations = [
        migrations.RunPython(read_excel_timetable),
    ]
