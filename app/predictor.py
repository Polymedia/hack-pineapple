import sqlite3
import pandas as pd
from sklearn.linear_model import LogisticRegression

class Predictor:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        factors, model = self._model()
        self.factors = factors
        self.model = model

    def factors(self):
        return self.factors

    def probability(self, person):
        disease = self._disease(person)
        values = [getattr(person, f, None) for f in self.factors]
        values[len(values) - 1] = 1 if disease else 0
        return self.model.predict_proba(values)[0][1] * 100

    def probabilities(self, person, factor, values):
        disease = self._disease(person)
        probs = []
        for value in values:
            print(values)
            setattr(person, factor, value)
            pvalues = [getattr(person, f, None) for f in self.factors]
            pvalues[len(pvalues) - 1] = 1 if disease else 0
            prob = self.model.predict_proba(pvalues)[0][1] * 100
            probs.append(prob)
        return probs

    def _disease(self, person):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        disease = cursor.execute('''select count(person.id) from disease
            inner join person on person.id = disease.id_person
            where person.id = ? and disease.disease ="Гепатит"
            group by person.id''', (person.id,)).fetchall()
        return disease

    def _model(self, disease='Инфаркт'):
        persons = self.cursor.execute(
            '''select person.id,(strftime('%Y', 'now') - strftime('%Y', birthday)), smoker,diabet, weight,pressure_l,pressure_h,pulse FROM person''').fetchall()
        static_factors = ['id', 'age', 'smoker', 'diabet', 'weight', 'pressure_l', 'pressure_h', 'pulse']
        diseases = self.cursor.execute('''SELECT DISTINCT disease from disease''').fetchall()
        diseases = list(map(lambda x: x[0], diseases))
        data = pd.DataFrame(persons, columns=static_factors)

        for key in diseases:
            series = self.cursor.execute('''select person.id, case when disease.disease = ? then 1 else 0 end from disease
        inner join person on person.id = disease.id_person
        group by disease.id_person''', (key,)).fetchall()
            series = pd.Series(map(lambda x: x[1], series))
            if key in (disease, "Гепатит"): data[key] = series

        values = data[disease]
        del data[disease]
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

        model = LogisticRegression() #n_estimators=100, max_features='sqrt'
        model.fit(data, values)

        return data.columns, model
