from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Venda, ItemVenda

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    readonly_fields = ['subtotal']

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero_venda', 'cliente', 'vendedor', 'data_venda', 'status', 'total']
    list_filter = ['status', 'forma_pagamento', 'data_venda', 'vendedor']
    search_fields = ['numero_venda', 'cliente__nome']
    readonly_fields = ['numero_venda', 'data_venda']
    inlines = [ItemVendaInline]
    
    fieldsets = (
        (_('InformaÃ§Ãµes da Venda'), {
            'fields': ('numero_venda', 'data_venda', 'cliente', 'vendedor', 'status')
        }),
        (_('Pagamento'), {
            'fields': ('forma_pagamento', 'subtotal', 'desconto', 'total')
        }),
        (_('ObservaÃ§Ãµes'), {
            'fields': ('observacoes',)
        }),
    )

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'quantidade', 'preco_unitario', 'subtotal']
    list_filter = ['venda__data_venda']
    search_fields = ['venda__numero_venda', 'produto__nome']
