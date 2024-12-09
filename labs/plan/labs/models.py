from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin
from django.contrib.postgres import fields


class Building(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Building: {self.name}'


class Flour(models.Model):
    name = models.CharField(max_length=255, blank=False)
    institute = models.ForeignKey(
        "Building",
        on_delete=models.CASCADE,
        related_name="building",
        blank=True,
        null=True)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Building: {self.name}'


class Audience(models.Model):
    number = models.CharField(max_length=150, blank=True)
    building = models.ForeignKey(
        "Building",
        on_delete=models.CASCADE,
        related_name="building_audience",
        blank=True,
        null=True)
    flour = models.ForeignKey(
        "Flour",
        on_delete=models.CASCADE,
        related_name="flour_audience",
        blank=True,
        null=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'Audience: {self.number}|{self.building.name}'