from django.shortcuts import render
from django.http import HttpResponse
from tokens.models import Token
from tokens.serializers import NewTokenSerializer, TokenSerializer, TokenStatusUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
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
        print("__________________________")
        print("Serializse.data inside generate token fix", serializer.data)
        return next_token

@api_view(["GET"])
def list_tokens(request):
    tokens = Token.objects.all().order_by('-token_number')
    serializer = TokenSerializer(tokens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
# mark token as completed or skipped
@api_view(["PUT"])
def update_token_status(request, token_number):
    token_instance = Token.objects.filter(token_number=token_number).first()
    
    if not token_instance:
        return Response({"error": "Token not found."}, status=404)
    
    serializer = TokenStatusUpdateSerializer(token_instance,request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Token {token_number} updated successfully."}, status=200)
    return Response(serializer.errors, status=400)

# list pending tokens for the day
@api_view(["GET"])
def list_pending_tokens(request):
    tokens = Token.objects.filter(status="pending")
    
    serializer = TokenSerializer(tokens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)