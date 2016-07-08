#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base, declared_attr

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
    birthday = Column(Date)
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