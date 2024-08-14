from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)


class Access(models.Model):
    description = models.CharField(max_length=255, blank=False)


class InstituteGroup(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)


class Preferences(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=False)
