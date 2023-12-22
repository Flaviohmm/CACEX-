from django.contrib import admin
from .models import Nome, Setor, Municipio, Atividade, RegistroAtividade

@admin.register(Nome)
class NomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('id', 'setor')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'municipio')

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'atividade') 

@admin.register(RegistroAtividade)
class RegistroAtividadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'setor', 'municipio', 'atividade', 'descricao_atividade', 'data_recepcao', 'data_inicio', 'data_fim', 'duracao_dias', 'observacao', 'status')    