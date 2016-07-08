"""
Definition of views.
"""
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Person
from app.models import Disease
from app.predictor import Predictor


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
    predictor = Predictor(path=None)
    pred_probs = predictor.probabilities(patient_id,
                                         factor=None,
                                         values=None)
    context = {'person': person,
               'diseases': diseases,
               'predictions': pred_probs}
    return render(request=request,
                  template_name='app/patient/prediction.html',
                  context=context)


def show_patient_prediction_details(request, patient_id):
    person = Person.objects.get(id=patient_id)
    diseases = Disease.objects.filter(id_person=patient_id).order_by('start_date')
    predictor = Predictor(path=None)
    context = {'person': person,
               'diseases': diseases,
               'predictor': predictor}
    return render(request=request,
                  template_name='app/patient/prediction_details.html',
                  context=context)
