from django.shortcuts import render
from django.http import HttpResponse
from tokens.models import Token
from tokens.serializers import NewTokenSerializer
# Create your views here.

def generate_token(patient_id):
    # get current token number
    current_token = Token.objects.order_by('-token_number').first()
    if current_token is None:
        next_token = 1
    else:
        next_token = current_token.token_number + 1
        
    # make entry in token table
    data = {'token_number': next_token,
            'patient':patient_id}
    serializer = NewTokenSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return next_token
