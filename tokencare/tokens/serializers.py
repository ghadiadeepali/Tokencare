from rest_framework import serializers
from tokens.models import Token

class NewTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["token_number","patient"]