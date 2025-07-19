from django.shortcuts import render
from tokens.models import Token
from tokens.serializers import TokenSerializer
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.decorators import api_view
from patients.models import Patient
from tokens.views import generate_token
from patients.tasks import send_token_message
from patients.serializers import NewPatientSerializerStaff

# staff registers a new patient
@api_view(["POST"])
def register_patient(request):
    phone_no = request.data.get('phone_no')
    name = request.data.get('name')
    # check if patient exists
    patient = Patient.objects.filter(phone_no=phone_no,name=name).first()
    if patient:
        # check if token already generated
        db_token = Token.objects.filter(patient=patient.id).first()
        if not db_token:
            token = generate_token(patient_id=patient.id)
        else:
            token = db_token.token_number
        # send_token_message.delay(phone_no, token)
        return Response({"msg": f"Your token number is {token}"})
        
    # add new patient
    serializer = NewPatientSerializerStaff(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        token   = generate_token(patient_id=patient.id) 
        
        # send message 
        send_token_message.delay(phone_no, token)
        return Response({"msg": f"Patient registered successfully. Your token number is {token}"},
                        status=status.HTTP_201_CREATED)

    # Validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    