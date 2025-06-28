from rest_framework import serializers
from patients.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        
        
class NewPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name', 'phone_no', 'age']
    