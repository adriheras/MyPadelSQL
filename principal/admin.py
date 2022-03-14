from django.contrib import admin

from principal.models import Historico, Jugador, Temporada

admin.site.register(Jugador)
admin.site.register(Historico)
admin.site.register(Temporada)
