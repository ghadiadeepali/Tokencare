from django.urls import path
from patients.views import get_patients, add_patient

urlpatterns = [
    path('',get_patients),
    path("add/",add_patient)
]