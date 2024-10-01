from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin
from django.contrib.postgres import fields


class Institute(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Institute: {self.name}'


class Building(models.Model):
    name = models.CharField(max_length=255, blank=False)
    institute = models.ForeignKey(
        "Institute",
        on_delete=models.CASCADE,
        related_name="institute",
        blank=True,
        null=True)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Building: {self.name}'


class AudienceStatus(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'Status: {self.name}'


class Audience(models.Model):
    number = models.CharField(max_length=150, blank=True)
    building = models.ForeignKey(
        "Building",
        on_delete=models.CASCADE,
        related_name="building",
        blank=True,
        null=True)
    number_of_users = models.IntegerField(default=1)
    audience_status = models.ForeignKey(
        "AudienceStatus",
        on_delete=models.CASCADE,
        related_name="audience_status_audience",
        blank=True,
        null=True)
    day_history = models.ForeignKey(
        "DayHistory",
        on_delete=models.CASCADE,
        related_name="day_history_audience",
        blank=True,
        null=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'Audience: {self.number}|{self.building.name}'


class UsersWallet(models.Model):
    username = models.CharField(max_length=255, blank=True)
    token = models.CharField(max_length=255, blank=True)
    number_bb = models.FloatField()

    def __str__(self):
        return f'UsersWallet: {self.username}|{self.number_bb}'


class Book(models.Model):
    audience = models.ForeignKey(
        "Audience",
        on_delete=models.CASCADE,
        related_name="audience",
        blank=True,
        null=True)
    user = models.ForeignKey(
        "UsersWallet",
        on_delete=models.CASCADE,
        related_name="users_wallet",
        blank=True,
        null=True)
    number_bb = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(28.0)],)
    pair_number = models.IntegerField(default=0)
    date = models.DateField()
    booking_time = models.TimeField(auto_now_add=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'Book: {self.user.username}|{self.number_bb}'


class BookHistory(models.Model):
    audience = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, blank=True)
    number_bb = models.FloatField(default=0.0)
    pair_number = models.IntegerField(default=0)
    date = models.DateField()
    booking_time = models.TimeField(auto_now_add=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'Book|A:{self.audience}|U:{self.user}|P:{self.pair_number}|N:{self.number_bb}'


class BookPair(models.Model):
    user = models.ForeignKey(
        "UsersWallet",
        on_delete=models.CASCADE,
        related_name="users_wallet_book_pair",
        blank=True,
        null=True)
    number_bb = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(28.0)],)
    pair_number = models.IntegerField(default=0)
    booking_time = models.TimeField(auto_now_add=True)
    audience_status = models.ForeignKey(
        "AudienceStatus",
        on_delete=models.CASCADE,
        related_name="audience_status_book_pair",
        blank=True,
        null=True)

    def set_attributes_from_name(self, name):
        pass

    def __str__(self):
        return f'Book: {self.user.username}|{self.number_bb}'


class DayHistory(models.Model):
    audience = models.ForeignKey(
        "Audience",
        on_delete=models.CASCADE,
        related_name="audience_day_history",
        blank=True,
        null=True)
    #tags = fields.ArrayField(
    #    BookPair(
    #        number_bb=0,
    #        pair_number=0
    #    ),
    #    blank=True,
    #    null=True)
    #pair = models.ArrayField(
    #    BookPair(
    #        number_bb=0,
    #        pair_number=0
    #    ),
    #    size=8,
    #)
    pair = fields.ArrayField(
        fields.ArrayField(
            models.CharField(max_length=255, blank=True),
            max_length=8,
            blank=True,
            null=True
        ),
        max_length=8,
        blank=True,
        null=True
    )
    #pieces = fields.ArrayField(fields.ArrayField(models.IntegerField()))
    date = models.DateField()
    booking_time = models.TimeField(auto_now_add=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'Book|A:{self.audience}|D:{self.date}'


@admin.register(DayHistory)
class DayHistoryAdmin(admin.ModelAdmin):
    search_fields = ("id", "audience", "date", "booking_time")
    list_display = ("id", "audience", "date", "booking_time", )


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "institute", "description")
    list_display = ("id", "name", "institute", )


@admin.register(AudienceStatus)
class AudienceStatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", "description", )


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    search_fields = ("id", "number", "building", "description")
    list_display = ("id", "number", "building", "number_of_users", "audience_status",)


@admin.register(UsersWallet)
class UsersWalletAdmin(admin.ModelAdmin):
    search_fields = ("id", "username", "number_bb")
    list_display = ("id", "username", "number_bb", )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time")
    list_display = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time", )


@admin.register(BookHistory)
class BookHistoryAdmin(admin.ModelAdmin):
    search_fields = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time")
    list_display = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time", )
