# Generated by Django 4.1.3 on 2024-08-15 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_user_third_name_alter_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='preferences',
            field=models.ManyToManyField(blank=True, null=True, to='main.preferences'),
        ),
    ]
