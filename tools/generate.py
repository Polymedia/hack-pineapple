#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from faker import Factory
import random
from datetime import datetime, timedelta
from decimal import Decimal
import sqlalchemy.types as types

Base = declarative_base()

class Numeric(types.TypeDecorator):
    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return float(Decimal(value))

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    sex = Column(Boolean)
    name = Column(String)
    last_name = Column(String)
    bitrhday = Column(Date)
    smoker = Column(Boolean)
    diabet = Column(Boolean)
    weight = Column(Numeric)
    pressure_l = Column(Integer)
    pressure_h = Column(Integer)
    pulse = Column(Numeric)
    had_surgery = Column(Boolean)
    blood_type = Column(Integer)

class Disease(Base):
    __tablename__ = 'disease'

    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    id_person = Column(Integer)
    analys = Column(String)
    medicaments = Column(String)
    medical_report = Column(String)
    disease = Column(String)
    chronical = Column(Boolean)
    surgery = Column(Boolean)

fake = Factory.create('ru_RU')

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def infarct_prob(p):
    return -0.083 + 0.142 * int(p.smoker) + 0.009 * p.weight + 0.007 * p.pressure_l - 0.010 * p.pulse

# Connect to database
connectionString = 'postgresql://postgres:1@192.168.129.69:5432/data'
connectionString = 'sqlite:///hospital.db'

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Values
binary = [True, False]
illnesses = ['ОРЗ', 'ОРВИ', 'Ангина', 'Гепатит', 'Коньюктивит', 'Инсульт']

# Generate people
for i in range(0, 1000):
    faker = fake.simple_profile()
    fullname = faker['name']
    fullname = fullname.split(' ')

    person = Person()
    person.id = i
    person.sex = True if faker["sex"] == 'M' else False
    person.name = fullname[1]
    person.last_name = fullname[0]
    person.birthdate = datetime.strptime(faker['birthdate'], '%Y-%M-%d')
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
    pos = random.randrange(0, osm) if prob > 0.8 else -1
    last_date = random_date(person.birthdate, datetime.now())

    #print(prob)

    for j in range(0, osm):
        ds = random.randrange(120, 365)
        de = random.randrange(3, 15)

        illness = 'Инфаркт' if pos == j else random.choice(illnesses)

        disease = Disease()
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

    session.commit()

'''persons = session.query(Person).all()
for person in persons:
    print(person.__dict__)'''