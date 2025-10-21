from django.contrib import admin
from .models import DetecaoAudio, locais_explorado,Jogador
# Register your models here.

admin.site.register(DetecaoAudio)
admin.site.register(locais_explorado)
admin.site.register(Jogador)