from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Car(models.Model):
    mark = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    body = models.CharField(max_length=25)
    licence_plate = models.CharField(max_length=8, unique=True)
    transmission = models.CharField(max_length=25)
    clas = models.CharField(max_length=25)
    release_year = models.IntegerField()
    engine_capacity = models.FloatField()
    passengers = models.IntegerField(default=1)
    price_day = models.IntegerField()
    photo = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.mark + " " + self.model + " - " + self.licence_plate

class Manager(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE, default=2, primary_key=True)
    badge_number = models.IntegerField()
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.full_name

class Renter(models.Model):
    full_name = models.CharField(max_length=100, help_text=u'Фамилия Имя Отчество')
    email = models.EmailField(help_text=u'Email')
    phone = models.CharField(max_length=13, help_text=u'Телефон')
    age = models.IntegerField()
    passport = models.CharField(max_length=8, help_text=u'Серия и номер пасспорта')
    driving_experience = models.FloatField(help_text=u'2.0')

    def __str__(self):
        return self.full_name + " " + self.passport

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()
    author_name = models.CharField(max_length=100, help_text=u'Введите имя')
    text = models.CharField(max_length=5000, help_text=u'Текст отзыва')

    def __str__(self):
        return str(self.car) + " " + str(self.publication_date)

class Rent(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    day_start = models.DateField(u'День начала')
    day_end = models.DateField(u'День окончания')
    pickup_point = models.CharField(max_length=255)
    start_time = models.TimeField(u'Время подачи')
    end_time = models.TimeField(u'Время возврата')
    return_point = models.CharField(max_length=255)
    notes = models.TextField(u'Комментарий', blank=True, null=True)
    price = models.IntegerField(default=0)

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def clean(self):
        if self.day_end <= self.day_start:
            raise ValidationError('Дата окончания должна быть позже, чем дата начала')

        events = Rent.objects.filter(car=self.car)
        events_time = Rent.objects.filter(car=self.car, day_start=self.day_start)
        if events.exists():
            for event in events:
                if self.check_overlap(event.day_start, event.day_end, self.day_start, self.day_end):
                    raise ValidationError('Пересечение с другим контрактом: ' + str(event.day_start) + '-' + str(event.day_end))
        if events_time.exists():
            for event in events_time:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError('Пересечение с другим контрактом в день: ' + str(event.day_start) + " " + str(event.start_time) + '-' + str(event.end_time))