from django.shortcuts import render
from django.db import IntegrityError
from patients.serializers import PatientSerializer, NewPatientSerializer
from rest_framework import  status
from patients.models import Patient
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(["GET"])
def get_patients(request):
    patients = Patient.objects.all()
    
    if patients:
        output_serializer = PatientSerializer(patients, many=True)
        return Response(output_serializer.data)
    return Response({"message": "Patients not found"})

@api_view(["POST"])
def add_patient(request):
    serializer = NewPatientSerializer(data = request.data)
    if serializer.is_valid():
        try:
            patient = serializer.save()
            output = PatientSerializer(patient)
            return Response(output.data, status=201)
        except IntegrityError:
            return Response(
                {"error": "Patient with this phone number already exists. Hence token number will be provided"})
    return Response({"msg":serializer.errors})
    