"""
Definition of urls for pineapple.
"""
from django.conf.urls import url
import app.views


urlpatterns = [

    url(r'^$', app.views.home, name='home'),
    url(r'^history$', app.views.history, name='history'),
    url(r'^history/patient/(?P<patient_id>[0-9]+)$',
        view=app.views.show_patient_info,
        name='patient_history'),
    url(r'^history/patient/(?P<patient_id>[0-9]+)/prediction$',
        view=app.views.show_patient_prediction,
        name='patient_diseases_prediction'),
    url(r'^history/patient/(?P<patient_id>[0-9]+)/prediction'
        r'/(?P<prediction_path>detailes)',
        view=app.views.show_patient_prediction_details,
        name='patient_diseases_prediction_details')
]
