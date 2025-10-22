from django.contrib import admin
from .models import DetecaoAudio, locais_explorado,Jogador,Itens,Inventario
# Register your models here.

admin.site.register(DetecaoAudio)
admin.site.register(locais_explorado)
admin.site.register(Jogador)
admin.site.register(Itens)
admin.site.register(Inventario)