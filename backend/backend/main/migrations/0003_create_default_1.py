# Generated by Django 4.1.3 on 2024-08-20 01:48

from django.db import migrations, models


def populate_products(apps, schema_editor):
    # Создаём список поддерживаемых институтов
    Institute = apps.get_model('main', 'Institute')
    inst_1 = Institute.objects.create(name='МФТИ', description='Московский Физико-Технический Институт')
    inst_2 = Institute.objects.create(name='МГУ', description='Московский Государственный Университет')

    # Создаём здания для созданный ранее институтов
    Building = apps.get_model('main', 'Building')
    build_1 = Building.objects.create(name='ГК', description='Главный корпус', institute=inst_1)
    build_2 = Building.objects.create(name='ЛК', description='Лабораторный корпус', institute=inst_1)
    build_3 = Building.objects.create(name='ВМК', description='Корпус ВМК', institute=inst_2)

    # Создаем список статусов бронирования
    AudienceStatus = apps.get_model('main', 'AudienceStatus')
    audience_status_1 = AudienceStatus.objects.create(name='Свободно', description='Аудитория свободна')
    audience_status_2 = AudienceStatus.objects.create(name='Занято', description='Аудитория занята')
    audience_status_3 = AudienceStatus.objects.create(name='Скоро освободиться', description='Аудитория скоро освободиться')
    audience_status_4 = AudienceStatus.objects.create(name='Отсутствует для бронирования', description='Аудитория отсутствует для бронирования')

    # Создаем аудитории для бронирования
    Audience = apps.get_model('main', 'Audience')
    audience_list_mipt = ['511', '512', '513', '514', '432', '431', '429', '427', '425']
    for item in  audience_list_mipt:
        Audience.objects.create(
            number=item,
            description=f'Аудитория №{item}',
            building=build_1,
            audience_status=audience_status_1,
            number_of_users=20)

    # Создаём кошельки пользователей для оплаты бронирования
    UsersWallet = apps.get_model('main', 'UsersWallet')
    UsersWallet.objects.create(username='st2257', token='sdfhvkj87bvsoi', number_bb=28)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_audience_description'),
    ]

    operations = [
        migrations.RunPython(populate_products),
    ]
