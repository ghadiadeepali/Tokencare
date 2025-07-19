from django.db import models

# Create your models here.
class RoleChoices(models.TextChoices):
    ADMIN        = "admin", "Admin"
    RECEPTIONIST = "receptionist", "Receptionist"
    DOCTOR       = "doctor", "Doctor"

class Staff(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Use hashed password
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"