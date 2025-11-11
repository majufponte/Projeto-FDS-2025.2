from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Partida(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class DetecaoAudio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    detectado = models.BooleanField(default=False)
    if detectado:
        def __str__(self):
            return f"{self.usuario} - detectado"

class locais_explorado(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    partida=models.ForeignKey(Partida, on_delete=models.CASCADE)
    id_do_local=models.IntegerField()
    def __str__(self):
        return f"{self.usuario} explorou o local: {self.id_do_local}"

class Jogador(models.Model):
    partida=models.ForeignKey(Partida, on_delete=models.CASCADE)
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    nome=models.CharField(max_length=50)
    def __str__(self):
        return self.nome

class Itens(models.Model):
    nome=models.CharField(max_length=50)
    tipo=models.IntegerField()
    descricao=models.TextField()
    def __str__(self):
        return self.nome

class Inventario(models.Model):
    partida=models.ForeignKey(Partida, on_delete=models.CASCADE)
    jogador=models.ForeignKey(Jogador, on_delete=models.CASCADE)
    item=models.ForeignKey(Itens, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.jogador.nome} pegou {self.item.nome}"