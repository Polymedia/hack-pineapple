import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import psycopg2
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlite3

conn = sqlite3.connect('hospital2.db')
cur = conn.cursor()
#### DATABASE ####
Base = automap_base()
engine = create_engine('sqlite:///db.db')
#connectionString = 'postgresql://postgres:1@127.0.0.1:5432/postgres'
#engine = create_engine(connectionString)
Base.prepare(engine, reflect=True)
session = Session(engine)








def get_model(disease='Инфаркт'):
    persons = cur.execute('''with  dis as
(select id_person, disease from disease group by id_person having disease=?
union
select id_person, disease from disease group by id_person having disease!=?)


SELECT smoker,diabet,weight,pressure_l,pressure_h,pulse,disease FROM person
    join dis on dis.id_person = person.id; ''',(disease,disease)).fetchall()




    data = pd.DataFrame(persons)
    data.columns = ['smoker','diabet','weight','pressure_l','pressure_h','pulse','disease']
    values = [1 if x == 'Инфаркт' else 0 for x in data['disease']]
    data = data.ix[:,:-1]
    data['pulse'] = pd.to_numeric(data['pulse'])
    data['weight'] = pd.to_numeric(data['weight'])

    corr = data.corr()
    autocorr = []
    autocorr_dub = []
    for i in range(corr.shape[0]):
        for j in range(corr.shape[0]):
            if corr.ix[i,j] >0.9 and i!=j and corr.ix[:,i].name not in autocorr_dub:
                #print(corr.ix[:,i].name, corr.ix[:,j].name)
                autocorr.append(corr.ix[:,i].name)
                autocorr_dub.append(corr.ix[j,:].name)
    for name in autocorr:
        del data[name]

    ### Autoselect model
    # models = [LinearRegression(),  # метод наименьших квадратов
    #           RandomForestRegressor(n_estimators=100, max_features='sqrt'),  # случайный лес
    #           KNeighborsRegressor(n_neighbors=corr.shape[0]),  # метод ближайших соседей
    #           SVR(kernel='linear'),  # метод опорных векторов с линейным ядром
    #           LogisticRegression()  # логистическая регрессия
    #           ]
    #
    # Xtrn, Xtest, Ytrn, Ytest = train_test_split(data, values, test_size=0.2)
    # tmp = {"model": None,
    #        "r2Score": 0}
    # for model in models:
    #     # обучаем модель
    #     model.fit(Xtrn, Ytrn)
    #     # вычисляем коэффициент детерминации
    #     score  = r2_score(Ytest, model.predict(Xtest))
    #     print(score)
    #     if score > tmp['r2Score']:
    #         tmp['model'] = model
    #         tmp['r2Score'] = score

    model = LinearRegression()
    model.fit(data,values)
    print(data.corr())
    print(model.coef_)
    # print(predictions)
    return model

if __name__ == '__main__':
    # person = Base.classes.person(id=3,sex=True, name='1', smoker=True, diabet=False, weight=60, pressure_l=80,
    #                             pressure_h=120, pulse=100)
    # session.add(person)
    # session.commit()
    get_model()
    # persons = cur.execute('''SELECT * FROM person''').fetchall()
    # print(persons)