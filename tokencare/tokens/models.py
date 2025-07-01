from django.db import models
from patients.models import Patient

# Create your models here.
class Token(models.Model):
    
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        SKIPPED = 'skipped', 'Skipped'

    token_number = models.IntegerField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="tokens")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    # assigned_by = models.ForeignKey(default="User")
    called_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['token_number']
        indexes = [
            models.Index(fields=['token_number', 'created_at']),
        ]

    def __str__(self):
        return f"Token #{self.token_number} - {self.patient.name}"