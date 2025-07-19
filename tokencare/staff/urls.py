from django.urls import path
from staff.views import register_patient

urlpatterns = [
    path("add_patient/", register_patient)
]
