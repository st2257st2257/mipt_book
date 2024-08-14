from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Access(models.Model):
    description = models.CharField(max_length=255, blank=False)


class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    access_list = models.ManyToManyField(Access)


class InstituteGroup(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)


class Preferences(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)


class User(AbstractUser):
    third_name = models.CharField(max_length=150, blank=False)
    token = models.CharField(max_length=255, blank=False)
    book_rate = models.FloatField(default=7)
    institute_group = models.ForeignKey(
        InstituteGroup,
        on_delete=models.CASCADE,
        related_name="instituteGroup",
        default=lambda: InstituteGroup.objects.get(id=1))
    preferences = models.ManyToManyField(Preferences)
    #user_role = models.ForeignKey(
    #    Role,
    #    on_delete=models.CASCADE,
    #    related_name="user role")


@admin.register(Role)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )

@admin.register(Access)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "description")
    list_display = ("id", )

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
    search_fields = ("id", "third_name")
    list_display = ("id", "third_name", )
