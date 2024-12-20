from django.contrib import admin
from .models import Categoria, Entrada

# Definindo o admin para o modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')  # Exibe o nome da categoria e o usuário
    search_fields = ('nome',)  # Permite buscar por nome da categoria
    list_filter = ('usuario',)  # Filtro por usuário
    ordering = ('nome',)  # Ordena por nome da categoria

# Definindo o admin para o modelo Entrada
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'data_operacao', 'categoria', 'usuario')  # Exibe nome, valor, data, categoria e usuário
    search_fields = ('nome', 'descricao')  # Permite buscar por nome ou descrição da entrada
    list_filter = ('usuario', 'categoria', 'data_operacao')  # Filtros por usuário, categoria e data
    ordering = ('-data_operacao',)  # Ordena por data de operação (mais recentes primeiro)

# Registrando os modelos no admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Entrada, EntradaAdmin)
