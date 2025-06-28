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
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "No patients found"}, status=status.HTTP_400_NOT_FOUND)

@api_view(["POST"])
def add_patient_public_api(request):
    serializer = NewPatientSerializer(data = request.data)
    if serializer.is_valid():
        try:
            patient = serializer.save()
            output = PatientSerializer(patient)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"error": "Patient with this phone number already exists. Hence token number will be provided"}, status=status.HTTP_409_CONFLICT)
    return Response({"msg":serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    