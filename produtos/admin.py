from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome']
    list_editable = ['ativo']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'categoria', 'preco_venda', 'estoque_atual', 'ativo']
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['codigo', 'nome', 'codigo_barras']
    list_editable = ['preco_venda', 'ativo']
    readonly_fields = ['margem_lucro', 'criado_em', 'atualizado_em']
    
    fieldsets = (
        (_('InformaÃ§Ãµes BÃ¡sicas'), {
            'fields': ('codigo', 'nome', 'descricao', 'categoria', 'ativo')
        }),
        (_('PreÃ§os'), {
            'fields': ('preco_custo', 'preco_venda', 'margem_lucro')
        }),
        (_('Estoque'), {
            'fields': ('estoque_atual', 'estoque_minimo', 'unidade_medida')
        }),
        (_('Outros'), {
            'fields': ('codigo_barras',)
        }),
        (_('Datas'), {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
