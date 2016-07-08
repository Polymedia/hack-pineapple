class Predictor:
    def __init__(self, path):
        pass

    def factors(self):
        return {'1': "factor1",
                '2': "factor2",
                '3': 'factor3'}

    def probability(self, person):
        return 24.2

    def probabilities(self, person, factor, values):
        return list((1, 2, 3))
