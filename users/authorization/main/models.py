from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Access(models.Model):
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Access: {self.description}'


class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    access_list = models.ManyToManyField(Access)

    def __str__(self):
        return f'Role: {self.name}'


class InstituteGroup(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Institute Group: {self.name}'


class Preferences(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Preferences: {self.name}'


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
        return f'User: {self.username}'


@admin.register(Role)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(Access)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "description")
    list_display = ("id", "description")

@admin.register(InstituteGroup)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(Preferences)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(User)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "username", "first_name", "second_name", "third_name", "institute_group", "user_role", "book_rate")
    list_display = ("id", "username", "institute_group", "user_role", "book_rate",)
