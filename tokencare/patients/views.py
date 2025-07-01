from django.shortcuts import render
from django.db import IntegrityError
from patients.serializers import PatientSerializer, NewPatientSerializer, NewOTPSerializer ,OTPSerializer
from rest_framework import  status
from patients.models import Patient, OTP
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from django.utils import timezone
# Create your views here.

@api_view(["GET"])
def get_patients(request):
    patients = Patient.objects.all()
    output_serializer = PatientSerializer(patients, many=True)
    return Response(output_serializer.data, status=status.HTTP_200_OK)
    
# validate OTP and add new patient
@api_view(["POST"])
def add_patient_public_api(request):
    phone_no = request.data.get("phone_no")
    patient_name = request.data.get("name")
    otp = request.data.get("otp")
    
    # check if patient already exists
    if Patient.objects.filter(phone_no=phone_no, name=patient_name).exists():
        return Response({"error": "Patient already exists. Hence token number will be provided"}, status=status.HTTP_409_CONFLICT)
    
    # if not registered, check if otp generated for this number
    # can have multiple otp requests that are not expired
    otp_queryset = OTP.objects.filter(phone_no=phone_no, expires_at__gt=timezone.now()).order_by("-created_at")
    if not otp_queryset.exists():
        return Response({"detail": "Please request an OTP first."},
            status=status.HTTP_400_BAD_REQUEST)
        
    # check for latest otp
    latest_otp = otp_queryset.first()
    if latest_otp.expires_at < timezone.now():
        return Response({"msg": "OTP has expired. Please request a new one."}, status=400)

    if latest_otp.otp != otp:
        return Response({"msg": "Invalid OTP. Please try again."}, status=400)
    
         
    # validate and save new patient
    serializer = NewPatientSerializer(data = request.data)
    if serializer.is_valid():
        patient = serializer.save()
        output = PatientSerializer(patient)
        return Response(output.data, status=status.HTTP_201_CREATED)
                      
    return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    

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


