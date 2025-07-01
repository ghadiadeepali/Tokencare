from django.db import models
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(minutes=5)



# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone_no = models.CharField(max_length=10, blank=True, unique=True)
    age = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.id})"
    
class OTP(models.Model):
    phone_no = models.CharField(max_length=10, blank=True)
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=default_expiry)
    # is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # default_expiry() is called when the model is instantiated, not when the file is loaded
    # So you always get an expiry time based on the exact creation time
    
    class Meta:
        # 🧠 Composite index on (phone_no, expires_at) to speed up OTP verification
        # Most lookups filter by phone_no + check if OTP is still valid (not expired)
        # This index makes those queries significantly faster on large tables
        indexes = [models.Index(fields=["phone_no", "expires_at"]),]
        
        