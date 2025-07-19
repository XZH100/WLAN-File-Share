from django.db import models
from django.utils import timezone

def user_upload_path(instance, filename):
    return f"uploads/{instance.username}/{filename}"

class SharedFile(models.Model):
    username = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.file.name}"
