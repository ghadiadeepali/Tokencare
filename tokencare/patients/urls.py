from django.urls import path
from patients.views import get_patients, add_patient_public_api, generate_otp, sum

urlpatterns = [
    path('',get_patients),
    path("add/",add_patient_public_api),
    path("verify/generate_otp",generate_otp),
    path("sum/", sum)
]