from rest_framework import serializers
from patients import models

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = "__all__"
        
        
class NewPatientSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)
    class Meta:
        model = models.Patient
        fields = ['name', 'phone_no', 'age', "otp"]
        
    def create(self, validated_data):
        validated_data.pop('otp', None)  # 🚨 Remove otp before passing to model
        return models.Patient.objects.create(**validated_data)
    
class NewOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OTP
        fields = ["phone_no","otp"]
        
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OTP
        fields = "__all__"