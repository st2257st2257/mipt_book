from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields


class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Роль: {self.name}'


class Department(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Факультет: {self.name}'


class User(AbstractUser):
    third_name = models.CharField(max_length=150, blank=True)
    token = models.CharField(max_length=255, blank=True)
    book_rate = models.FloatField(default=7)
    institute_group = models.ForeignKey(
        "InstituteGroup",
        on_delete=models.CASCADE,
        related_name="instituteGroup",
        blank=True,
        null=True)
    user_role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_role",
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.username}'

    def add_preference(self, preference_name):
        preference = Preferences.objects.filter(name=preference_name)
        if len(preference) == 1:
            self.preferences.add(preference[0])

    def remove_preference(self, preference_name):
        preference = Preferences.objects.filter(name=preference_name)
        if len(preference) == 1:
            self.preferences.remove(preference[0])