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
    week_pairs = fields.ArrayField(
        fields.ArrayField(  # дни недели
            fields.ArrayField(  # пары
                models.CharField(max_length=255, blank=True),
                max_length=8,
                blank=True,
                null=True
            ),
            max_length=20,
            blank=True,
            null=True
        ),
        max_length=7,
        blank=True,
        null=True
    )
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'Audience: {self.number}|{self.building.name}'

    def make_free(self, time_slot):
        self.day_history.pair[time_slot][1] = "Свободно"
        self.audience_status = AudienceStatus.objects.get(name="Свободно")
        self.day_history.save()
        self.save()

    def clear_booking(self, time_slot):
        if self.day_history.pair[time_slot][1] != "Отсутствует для бронирования":
            self.day_history.pair[time_slot][1] = "Свободно"
            self.audience_status = AudienceStatus.objects.get(name="Свободно")
        else:
            self.day_history.pair[time_slot][1] = "Отсутствует для бронирования"
            self.audience_status = AudienceStatus.objects.get(name="Отсутствует для бронирования")
        self.day_history.save()
        self.save()

    def make_all_free(self):
        for i in range(len(self.day_history.pair)):
            self.day_history.pair[i][1] = "Свободно"
        self.audience_status = AudienceStatus.objects.get(name="Свободно")
        self.day_history.save()
        self.save()

    def make_booked(self):
        # TODO: очистить дневную историю
        self.audience_status = AudienceStatus.objects.get("Занято")
        self.save()


class UsersWallet(models.Model):
    username = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
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
    time_slot = models.IntegerField(default=0)
    date = models.DateField()
    booking_time = models.TimeField(auto_now_add=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'Book: {self.user}|{self.number_bb}'

    def to_history(self):
        audience = Audience.objects.get(number=self.audience.number)
        audience.make_free(time_slot=self.pair_number)

        history_booking = BookHistory(
            audience=self.audience.number,  # CharField
            user=self.user.username,        # CharField
            number_bb=self.number_bb,       # FloatField
            pair_number=self.pair_number,   # IntegerField
            date=self.date,                 # DateField
            booking_time=self.booking_time, # TimeField
            visibility=self.visibility,     # IntegerField
        )
        history_booking.save()
        Book.objects.filter(id=self.id).delete()
        pass

    def clear_booked_audiences(self):
        pass


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
    pair = fields.ArrayField(
        fields.ArrayField(
            models.CharField(max_length=255, blank=True),
            max_length=8,
            blank=True,
            null=True
        ),
        max_length=20,
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
    search_fields = ("id", "date", "booking_time")
    list_display = ("id", "audience", "date", "booking_time", )


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", "institute", )


@admin.register(AudienceStatus)
class AudienceStatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description")
    list_display = ("id", "name", "description", )


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    search_fields = ("id", "number", "description")
    list_display = ("id", "number", "building", "number_of_users", "audience_status",)

    actions = ["make_free", "make_booked", "make_excluded", "make_all_free", "cancel_daily_booking"]

    @admin.action(description="Сделать свободными")
    def make_free(self, request, queryset):
        free_status = AudienceStatus.objects.get(name="Свободно")
        queryset.update(audience_status=free_status)

    @admin.action(description="Сделать занятыми")
    def make_booked(self, request, queryset):
        booked_status = AudienceStatus.objects.get(name="Занято")
        queryset.update(audience_status=booked_status)

    @admin.action(description="Исключить из бронирования")
    def make_excluded(self, request, queryset):
        excluded_status = AudienceStatus.objects.get(name="Отсутствует для бронирования")
        queryset.update(audience_status=excluded_status)

    @admin.action(description="Освободить все")
    def make_all_free(self, request, queryset):
        excluded_status = AudienceStatus.objects.get(name="Свободно")
        queryset.filter(audience_status__name="Занято").update(audience_status=excluded_status)
        queryset.filter(audience_status__name="Скоро освободиться").update(audience_status=excluded_status)

    @admin.action(description="Удалить бронирования на день")
    def cancel_daily_booking(self, request, queryset):
        excluded_status = AudienceStatus.objects.get(name="Свободно")
        queryset.filter(audience_status__name="Занято").update(audience_status=excluded_status)
        queryset.filter(audience_status__name="Скоро освободиться").update(audience_status=excluded_status)
        for item in queryset.filter():
            for i in range(len(item.day_history.pair)):
                item.day_history.pair[i][1] = "Свободно"
                item.day_history.save()
            item.save()


@admin.register(UsersWallet)
class UsersWalletAdmin(admin.ModelAdmin):
    search_fields = ("id", "username", "number_bb")
    list_display = ("id", "username", "number_bb", )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("id", "user", "number_bb", "pair_number", "date", "booking_time", "time_slot")
    list_display = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time", "time_slot",)

    actions = ["finish_booking", "stop_booking", "cancel_booking"]

    @admin.action(description="Завершить бронирование")
    def finish_booking(self, request, queryset):
        """ Завершение бронирования и перевод бронирования в историю """
        # TODO: добавить условие на снятие бронирования по нужному фильтру
        for booking in queryset:
            # Меняем статус аудитории
            audience = Audience.objects.get(number=booking.audience.number)
            free_status = AudienceStatus.objects.get(name="Свободно")
            audience.audience_status = free_status
            audience.save()
            # Переводим бронирование в историю
            booking.to_history()
        queryset.delete()

    @admin.action(description="Остановить бронирование")
    def stop_booking(self, request, queryset):
        """ Остановка бронирования. По определенной причине """
        # excluded_status = AudienceStatus.objects.get(name="Отсутствует для бронирования")
        # queryset.update(audience_status=excluded_status)
        pass

    @admin.action(description="Отменить бронирование")
    def cancel_booking(self, request, queryset):
        """ Отмена бронирования и перевод аудитории в статус свободной для бронирования """
        # excluded_status = AudienceStatus.objects.get(name="Отсутствует для бронирования")
        # queryset.update(audience_status=excluded_status)
        pass


@admin.register(BookHistory)
class BookHistoryAdmin(admin.ModelAdmin):
    search_fields = ("id", "number_bb", "pair_number", "date", "booking_time")
    list_display = ("id", "audience", "user", "number_bb", "pair_number", "date", "booking_time", )
