from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone_no = models.CharField(max_length=10, blank=True, unique=True)
    age = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.id})"