#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import random
from decimal import Decimal
from datetime import datetime, timedelta

from faker import Factory

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from tables import Base, Person, Disease

fake = Factory.create('ru_RU')

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def infarct_prob(p):
    return -0.083 + 0.142 * int(p.smoker) + 0.009 * p.weight + 0.007 * p.pressure_l - 0.010 * p.pulse

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Not enought arguments')

    # Connect to database
    connectionString = 'sqlite:///' + sys.argv[1]

    engine = create_engine(connectionString)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    # Values
    binary = [True, False]
    illnesses = ['ОРЗ', 'ОРВИ', 'Ангина', 'Гепатит', 'Коньюктивит', 'Инсульт']
    counter = 0

    # Generate people
    n = int(sys.argv[2])
    for i in range(0, n):
        faker = fake.simple_profile()
        fullname = faker['name']
        fullname = fullname.split(' ')

        person = Person()
        person.id = i
        person.sex = True if faker["sex"] == 'M' else False
        person.name = fullname[1]
        person.last_name = fullname[0]
        person.birthday = datetime.strptime(faker['birthdate'], '%Y-%M-%d')
        person.smoker = random.choice(binary)
        person.diabet = random.choice(binary)
        person.weight = random.uniform(40.0, 150.0)
        person.pressure_l = random.randrange(60, 100)
        person.pressure_h = person.pressure_l + random.randrange(25, 40)
        person.pulse = (person.pressure_l - 60) * 0.5 + random.randrange(70, 90)
        person.had_surgery = random.choice(binary)
        person.blood_type = random.randrange(0, 7)

        #print(person.__dict__)
        session.add(person)

        prob = infarct_prob(person)
        osm = random.randrange(3, 15)
        pos = random.randrange(0, osm) if prob > 0.5 else -1
        last_date = random_date(person.birthday, datetime.now())

        #print(prob)

        for j in range(0, osm):
            ds = random.randrange(120, 365)
            de = random.randrange(3, 15)

            illness = 'Инфаркт' if pos == j else random.choice(illnesses)

            disease = Disease()
            disease.id = counter
            disease.start_date = last_date + timedelta(days=ds)
            disease.end_date = disease.start_date + timedelta(days=de)
            disease.id_person = person.id
            disease.analys = ''
            disease.medicaments = ''
            disease.medical_report = ''
            disease.disease = illness
            disease.chronical = random.choice(binary)
            disease.surgery = random.choice(binary)

            #print(disease.__dict__)
            session.add(disease)

            counter = counter + 1

        session.commit()
