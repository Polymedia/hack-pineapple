"""
Definition of urls for pineapple.
"""
from django.conf.urls import url
import app.views


urlpatterns = [

    url(r'^$', app.views.home, name='home'),
    url(r'^history$', app.views.history, name='history'),
    url(r'^prediction', app.views.prediction, name='prediction'),
    url(r'^history/patient/(?P<patient_id>[0-9]+)$',
        view=app.views.show_patient,
        name='patient_history')

]
