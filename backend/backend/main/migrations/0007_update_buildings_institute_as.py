from django.db import migrations, models
import pandas as pd


def create_from_excel_institutes_buildings_audience_statuses(apps, schema_editor):
    """Заполняет таблицу базовыми значениями, забитыми в эксель файле"""
    """Заполняется: Институты, Здания, Статусы"""
    institutes = pd.read_excel("start_data.xlsx", sheet_name="Институты")
    buildings = pd.read_excel("start_data.xlsx", sheet_name="Здания")
    audience_statuses = pd.read_excel("start_data.xlsx", sheet_name="Статусы")

    # Создаём список поддерживаемых институтов
    Institute = apps.get_model('main', 'Institute')
    Institute.objects.all().delete()
    for inst in institutes.values:
        _institute = Institute.objects.create(
            name=inst[0],
            description=inst[1])

    # Создаём здания для созданный ранее институтов
    Building = apps.get_model('main', 'Building')
    Building.objects.all().delete()
    for building in buildings.values:
        institute = Institute.objects.get(name=building[0])
        _build = Building.objects.create(
            name=building[1],
            description=building[2],
            institute=institute)
        _build.save()

    # Создаем список статусов бронирования
    AudienceStatus = apps.get_model('main', 'AudienceStatus')
    AudienceStatus.objects.all().delete()
    for audience_status in audience_statuses.values:
        _audience_status = AudienceStatus.objects.create(
            name=audience_status[0],
            description=audience_status[1])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_dayhistory_pair'),
    ]

    operations = [
        migrations.RunPython(create_from_excel_institutes_buildings_audience_statuses),
    ]

