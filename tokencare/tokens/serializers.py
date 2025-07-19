from rest_framework import serializers
from tokens.models import Token

class NewTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["token_number","patient"]
        
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"
        
class TokenStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["status"]