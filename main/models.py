from django.db import models

from django.contrib.auth.models import User

class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    #email = models.EmailField() 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)  # Store detailed analysis results

    # def __str__(self):
    #     return f"{self.user.username} - {self.email}"
