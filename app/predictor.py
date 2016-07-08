import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

class Predictor:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        factors, model = self._model()
        self.factors = factors
        self.model = model

    def factors(self):
        return self.factors

    def probability(self, person):
        values = [person.__dict__[f] for f in self.factors]
        return self.model.predict(values)[0] * 100

    def probabilities(self, person, factor, values):
        probs = []
        for value in values:
            setattr(person, factor, value)
            pvalues = [person.__dict__[f] for f in self.factors]
            prob = self.model.predict(pvalues)[0] * 100
            probs.append(prob)
        return probs

    def _model(self, disease='Инфаркт'):
        persons = self.cursor.execute('''
        with  dis as
        (select id_person, disease from disease group by id_person having disease=?
        union
        select id_person, disease from disease group by id_person having disease!=?)


        SELECT smoker,diabet,weight,pressure_l,pressure_h,pulse,disease FROM person
        join dis on dis.id_person = person.id
        ''',(disease, disease)).fetchall()

        data = pd.DataFrame(persons)
        data.columns = ['smoker', 'diabet', 'weight', 'pressure_l', 'pressure_h', 'pulse', 'disease']
        values = [1 if x == 'Инфаркт' else 0 for x in data['disease']]
        data = data.ix[:,:-1]
        # sqlite3 has no decimap support
        data['pulse'] = pd.to_numeric(data['pulse'])
        data['weight'] = pd.to_numeric(data['weight'])

        corr = data.corr()
        autocorr = []
        autocorr_dub = []
        for i in range(corr.shape[0]):
            for j in range(corr.shape[0]):
                if corr.ix[i,j] > 0.9 and i != j and corr.ix[:,i].name not in autocorr_dub:
                    autocorr.append(corr.ix[:,i].name)
                    autocorr_dub.append(corr.ix[j,:].name)
        
        # Remove autocorrelation
        for name in autocorr:
            del data[name]

        model = LinearRegression()
        model.fit(data, values)

        return data.columns, model
