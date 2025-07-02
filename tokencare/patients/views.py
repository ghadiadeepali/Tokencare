from django.shortcuts import render
from django.db import IntegrityError
from patients.serializers import PatientSerializer, NewPatientSerializer, NewOTPSerializer ,OTPSerializer
from rest_framework import  status
from patients.models import Patient, OTP
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from django.utils import timezone
from tokens.views import generate_token
from tokens.models import Token
from patients.tasks import add_numbers
# Create your views here.

@api_view(["GET"])
def get_patients(request):
    patients = Patient.objects.all()
    output_serializer = PatientSerializer(patients, many=True)
    return Response(output_serializer.data, status=status.HTTP_200_OK)
    
# validate OTP and add new patient
# validate OTP and add new patient
@api_view(["POST"])
def add_patient_public_api(request):
    phone_no = request.data.get("phone_no")
    patient_name = request.data.get("name")
    otp_input = request.data.get("otp") 

    # If patient already exists, just return a fresh token
    patient = Patient.objects.filter(phone_no=phone_no, name=patient_name).first()
    if patient:
        # check if token already generated
        db_token = Token.objects.filter(patient=patient.id).first()
        if not db_token:
            token = generate_token(patient_id=patient.id)
        else:
            token = db_token.token_number
        return Response({"msg": f"Your token number is {token}"})

    # Latest *valid* OTP (expired ones are already purged by Celery)
    latest_otp = (OTP.objects.filter(phone_no=phone_no, expires_at__gt=timezone.now()).order_by("-created_at").first())

    if latest_otp is None:
        return Response({"detail": "OTP is either expired or not generated. Please request OTP first."},status=status.HTTP_400_BAD_REQUEST)

    if latest_otp.otp != otp_input:
        return Response({"msg": "Invalid OTP. Please try again."},status=status.HTTP_400_BAD_REQUEST)

    # Passed OTP check – create the patient
    serializer = NewPatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        token   = generate_token(patient_id=patient.id) 
        return Response({"msg": f"Your token number is {token}"},
                        status=status.HTTP_201_CREATED)

    # Validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# generate OTP  
@api_view(["POST"])
def generate_otp(request):
    phone_no = request.data.get("phone_no")
    otp = str(random.randint(1000, 9999))
    
    payload = {
        "phone_no": phone_no,
        "otp": otp
    }
    # make otp entry in OTP table
    serializer = NewOTPSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        
        payload = {"message":f"OTP Sent Successfully on {phone_no}. Your OTP is {otp} and is valid for 5 minutes"}
        
        return Response(payload, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def sum(request):
    a = request.data.get("a")
    b = request.data.get("b")
    result = add_numbers.delay(a, b)
    
    return Response({
            "message": "Task submitted successfully",
            "task_id": result.id,
        })