"""
Definition of views.
"""
from copy import deepcopy
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Person
from app.models import Disease
from app.predictor import Predictor


predictor = Predictor(path='db.sqlite3')

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    people = Person.objects.all()
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
                                          {'title': 'Home Page',
                                           'people': people
                                           }
                                          )
    )


def history(request):
    assert isinstance(request, HttpRequest)
    return redirect('/')


def show_patient_info(request, patient_id):
    person = Person.objects.get(id=patient_id)
    diseases = Disease.objects.filter(id_person=patient_id).order_by('start_date')
    context = {'person': person,
               'diseases': diseases}
    return render(request=request,
                  template_name='app/patient/info.html',
                  context=context)


def show_patient_prediction(request, patient_id):
    person = Person.objects.get(id=patient_id)
    diseases = Disease.objects.filter(id_person=patient_id).order_by('start_date')
    pred_probs = {
        'Инфаркт': predictor.probability(person)
    }
    context = {'person': person,
               'diseases': diseases,
               'predictions': pred_probs}
    return render(request=request,
                  template_name='app/patient/prediction.html',
                  context=context)


def show_patient_prediction_details(request,
                                    patient_id):
    person = Person.objects.get(id=patient_id)
    diseases = Disease.objects.filter(id_person=patient_id).order_by('start_date')

    keys_age = [35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61]
    predictions_age = {
        'labels': list(map(str, keys_age))
    }

    keys_weight = [87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113]
    predictions_weight = {
        'labels': list(map(str, keys_weight))
    }

    person.smoker = False
    predictions_age['values'] = predictor.probabilities(deepcopy(person), 'age', keys_age)
    predictions_weight['values'] = predictor.probabilities(deepcopy(person), 'weight', keys_weight)

    person.smoker = True
    predictions_age['values_s'] = predictor.probabilities(deepcopy(person), 'age', keys_age)
    predictions_weight['values_s'] = predictor.probabilities(deepcopy(person), 'weight', keys_weight)

    context = {
        'person': person,
        'diseases': diseases,
        'predictions_age': predictions_age,
        'predictions_weight': predictions_weight
    }

    return render(request=request,
                  template_name='app/patient/prediction_details.html',
                  context=context)
