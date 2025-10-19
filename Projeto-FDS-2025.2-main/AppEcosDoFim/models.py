from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DetecaoAudio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    detectado = models.BooleanField(default=False)
    if detectado:
        def __str__(self):
            return f"{self.usuario} - detectado"

class locais_explorado(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    id_do_local=models.IntegerField()
    def __str__(self):
        return f"{self.usuario} explorou o local: {self.id_do_local}"