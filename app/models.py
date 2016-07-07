"""
Definition of models.
"""

from django.db import models


class Person(models.Model):
    sex = models.BooleanField()
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    birthdate = models.DateField()
    smoker = models.BooleanField()
    diabet = models.BooleanField()
    weight = models.FloatField()
    pressure_l = models.IntegerField()
    pressure_h = models.IntegerField()
    pulse = models.FloatField()
    had_surgery = models.BooleanField()
    blood_type = models.IntegerField()


class Desease(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    id_person = models.ForeignKey(Person)
    analysis = models.TextField()
    medicaments = models.TextField()
    medical_report = models.TextField()
    desease = models.TextField()
    chronical = models.BooleanField()
    surgery = models.BooleanField()

