# detection/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_scan_path(instance, filename):
    return f"scans/user_{instance.user.id}/{filename}"

class HairScan(models.Model):
    CLASS_CHOICES = [
        ('alopecia', 'Alopecia'),
        ('dandruff', 'Dandruff'),
        ('normal', 'Normal'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hair_scans")
    image = models.ImageField(upload_to=upload_scan_path)

    result = models.CharField(max_length=20, choices=CLASS_CHOICES, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.result or 'Pending'}"

class ProgressImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progress_image")
    image = models.ImageField(upload_to='progress_images/')

    def __str__(self):
        return f"Progress Image for {self.user.email}"