"""
Definition of models.
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models


class Person(models.Model):
    sex = models.BooleanField()
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    birthday = models.DateField()
    smoker = models.BooleanField()
    diabet = models.BooleanField()
    weight = models.FloatField()
    pressure_l = models.IntegerField()
    pressure_h = models.IntegerField()
    pulse = models.FloatField()
    had_surgery = models.BooleanField()
    blood_type = models.IntegerField()

    class Meta:
        db_table = 'person'

    @property
    def age(self):
        now = datetime.now()
        current_year = int(now.year)
        birth_year = int(self.birthday.year)
        return current_year - birth_year

    @age.setter
    def age(self, value):
        now = datetime.now()
        self.birthday = now - relativedelta(years=value)


class Disease(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    id_person = models.ForeignKey(db_column='id_person',
                                  to=Person)
    analysis = models.TextField(null=True)
    medicaments = models.TextField(null=True)
    medical_report = models.TextField(null=True)
    disease = models.TextField(null=True)
    chronical = models.BooleanField()
    surgery = models.BooleanField()

    class Meta:
        db_table = 'disease'
