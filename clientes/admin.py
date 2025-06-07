from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_pessoa', 'cpf_cnpj', 'telefone', 'cidade', 'ativo']
    list_filter = ['tipo_pessoa', 'ativo', 'uf', 'criado_em']
    search_fields = ['nome', 'cpf_cnpj', 'email', 'telefone']
    list_editable = ['ativo']
    
    fieldsets = (
        (_('InformaÃ§Ãµes Pessoais'), {
            'fields': ('nome', 'tipo_pessoa', 'cpf_cnpj', 'data_nascimento')
        }),
        (_('Contato'), {
            'fields': ('email', 'telefone')
        }),
        (_('EndereÃ§o'), {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep')
        }),
        (_('Outros'), {
            'fields': ('observacoes', 'ativo', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['criado_em', 'atualizado_em']
