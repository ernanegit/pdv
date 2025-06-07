from django.db import models
from django.utils.translation import gettext_lazy as _

class Cliente(models.Model):
    TIPO_PESSOA_CHOICES = [
        ('F', _('Pessoa FÃ­sica')),
        ('J', _('Pessoa JurÃ­dica')),
    ]
    
    nome = models.CharField(_('Nome'), max_length=200)
    tipo_pessoa = models.CharField(_('Tipo de Pessoa'), max_length=1, choices=TIPO_PESSOA_CHOICES, default='F')
    cpf_cnpj = models.CharField(_('CPF/CNPJ'), max_length=18, blank=True)
    email = models.EmailField(_('E-mail'), blank=True)
    telefone = models.CharField(_('Telefone'), max_length=20, blank=True)
    endereco = models.CharField(_('EndereÃ§o'), max_length=200, blank=True)
    numero = models.CharField(_('NÃºmero'), max_length=10, blank=True)
    complemento = models.CharField(_('Complemento'), max_length=100, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=100, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True)
    uf = models.CharField(_('UF'), max_length=2, blank=True)
    cep = models.CharField(_('CEP'), max_length=10, blank=True)
    data_nascimento = models.DateField(_('Data de Nascimento'), blank=True, null=True)
    observacoes = models.TextField(_('ObservaÃ§Ãµes'), blank=True)
    ativo = models.BooleanField(_('Ativo'), default=True)
    criado_em = models.DateTimeField(_('Criado em'), auto_now_add=True)
    atualizado_em = models.DateTimeField(_('Atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def endereco_completo(self):
        endereco_parts = []
        if self.endereco:
            endereco_parts.append(self.endereco)
        if self.numero:
            endereco_parts.append(f"nÂº {self.numero}")
        if self.complemento:
            endereco_parts.append(self.complemento)
        if self.bairro:
            endereco_parts.append(self.bairro)
        if self.cidade and self.uf:
            endereco_parts.append(f"{self.cidade}/{self.uf}")
        return ', '.join(endereco_parts)
