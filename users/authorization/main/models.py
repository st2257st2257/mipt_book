from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Access(models.Model):
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Доступ: {self.description}'


class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    access_list = models.ManyToManyField(Access)

    def __str__(self):
        return f'Роль: {self.name}'


class Institute(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'ВУЗ: {self.name}'


class InstituteGroup(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    institute = models.ForeignKey(
        "Institute",
        on_delete=models.CASCADE,
        related_name="institute",
        blank=True,
        null=True)

    def __str__(self):
        return f'Группа ВУЗа: {self.name}'


class Preferences(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Предпочтение: {self.name}'


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
    preferences = models.ManyToManyField(
        Preferences,
        blank=True)
    user_role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_role",
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.username}'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(Access)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "description")
    list_display = ("id", "description")

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(InstituteGroup)
class InstituteGroupAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description", "institute")
    list_display = ("id", "name", "institute", )

@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "username", "first_name", "second_name", "third_name", "institute_group", "user_role", "book_rate")
    list_display = ("id", "username", "institute_group", "user_role", "book_rate",)
