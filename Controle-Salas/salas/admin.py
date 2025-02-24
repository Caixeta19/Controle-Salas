from django.contrib import admin
from .models import Sala, Agendamento

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade')
    search_fields = ('nome',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('sala', 'usuario', 'data', 'horario_inicio', 'horario_fim')
    list_filter = ('sala', 'data')  # Filtros laterais no admin
    search_fields = ('usuario__username', 'sala__nome')  # Busca por nome do usuário ou sala
