"""
Definition of views.
"""
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Person
from app.models import Disease


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


# def contact(request):
#     """Renders the contact page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         })
#     )def contact(request):
#     """Renders the contact page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         })
#     )


# def about(request):
#     """Renders the about page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/about.html',
#         context_instance = RequestContext(request,
#         {
#             'title':'About',
#             'message':'Your application description page.',
#             'year':datetime.now().year,
#         })
#     )


def history(request):
    assert isinstance(request, HttpRequest)
    return redirect('/')


def prediction(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/prediction.html',
        context_instance = RequestContext(request,
        {

        })
    )


def show_patient(request, patient_id):
    person = Person.objects.get(id=patient_id)
    diseases = Disease.objects.filter(id_person=patient_id)
    context = {'person': person,
               'diseases': diseases}
    return render(request=request,
                  template_name='app/history.html',
                  context=context)
