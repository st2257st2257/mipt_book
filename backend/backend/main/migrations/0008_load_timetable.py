import django.contrib.postgres.fields
from django.db import migrations, models
import pandas as pd
import datetime


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


def update_excel_audiences(apps, schema_editor):
    """Заполняет таблицу базовыми значениями, забитыми в эксель файле"""
    """Заполняется: Аудитории, Кошельки"""
    audiences = pd.read_excel("start_data.xlsx", sheet_name="Аудитории")
    users_wallets = pd.read_excel("start_data.xlsx", sheet_name="Кошельки")

    # Создаем аудитории для бронирования
    Building = apps.get_model('main', 'Building')
    AudienceStatus = apps.get_model('main', 'AudienceStatus')
    Audience = apps.get_model('main', 'Audience')
    DayHistory = apps.get_model('main', 'DayHistory')
    # Building.objects.all().delete()
    # AudienceStatus.objects.all().delete()
    Audience.objects.all().delete()
    DayHistory.objects.all().delete()
    for audience in audiences.values:
        build = Building.objects.get(name=audience[1], institute__name=audience[0])
        audience_status = AudienceStatus.objects.get(name=audience[4])
        _audience = Audience.objects.create(
            number=str(audience[2]),
            description=audience[3],
            building=build,
            audience_status=audience_status,
            number_of_users=audience[5],
            day_history=DayHistory.objects.create(
                pair=[
                    [
                        TIME_SLOT_DICT[i+1],   #  время бронирования
                        "Свободно",            #  статус аудитории
                        "blank_user",          #  кто бронирует аудиторию
                        "0",                   #  число баллов бронирования
                        str(audience[5])       #  число человек, которое вмещает аудитория
                    ] for i in range(14)],
                date="2023-03-08"))


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0007_update_buildings_institute_as'),
    ]

    operations = [
        migrations.RunPython(update_excel_audiences),
    ]

