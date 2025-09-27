from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DetecaoAudio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    detectado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {'detectado'}"
