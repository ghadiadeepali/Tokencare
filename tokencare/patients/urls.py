from django.urls import path
from patients.views import get_patients, add_patient_public_api

urlpatterns = [
    path('',get_patients),
    path("add/",add_patient_public_api)
]