# Generated by Django 4.1.3 on 2024-08-14 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_role_access_list_user_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='institute_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instituteGroup', to='main.institutegroup'),
        ),
    ]
