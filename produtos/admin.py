# produtos/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome']
    list_editable = ['ativo']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['miniatura', 'codigo', 'nome', 'categoria', 'preco_venda', 'estoque_atual', 'ativo']
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['codigo', 'nome', 'codigo_barras']
    list_editable = ['preco_venda', 'ativo']
    readonly_fields = ['miniatura_grande', 'margem_lucro', 'criado_em', 'atualizado_em']
    
    fieldsets = (
        (_('Informações Básicas'), {
            'fields': ('codigo', 'nome', 'descricao', 'categoria', 'ativo')
        }),
        (_('Imagem'), {
            'fields': ('imagem', 'miniatura_grande')
        }),
        (_('Preços'), {
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
    
    def miniatura(self, obj):
        """Miniatura para lista"""
        if obj.imagem:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.imagem.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #f0f0f0; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666;">Sem imagem</div>'
        )
    miniatura.short_description = 'Imagem'
    
    def miniatura_grande(self, obj):
        """Imagem grande para detalhes"""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.imagem.url
            )
        return format_html(
            '<div style="width: 200px; height: 200px; background: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #6c757d;">📷<br>Nenhuma imagem</div>'
        )
    miniatura_grande.short_description = 'Preview da Imagem'