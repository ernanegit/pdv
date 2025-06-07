from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from produtos.models import Produto
from clientes.models import Cliente

class Venda(models.Model):
    STATUS_CHOICES = [
        ('P', _('Pendente')),
        ('C', _('ConcluÃ­da')),
        ('A', _('Cancelada')),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('D', _('Dinheiro')),
        ('C', _('CartÃ£o de CrÃ©dito')),
        ('B', _('CartÃ£o de DÃ©bito')),
        ('P', _('PIX')),
        ('H', _('Cheque')),
    ]
    
    numero_venda = models.CharField(_('NÃºmero da Venda'), max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Cliente'))
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Vendedor'))
    data_venda = models.DateTimeField(_('Data da Venda'), auto_now_add=True)
    status = models.CharField(_('Status'), max_length=1, choices=STATUS_CHOICES, default='P')
    forma_pagamento = models.CharField(_('Forma de Pagamento'), max_length=1, choices=FORMA_PAGAMENTO_CHOICES, default='D')
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(_('Desconto'), max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(_('Total'), max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(_('ObservaÃ§Ãµes'), blank=True)
    
    class Meta:
        verbose_name = _('Venda')
        verbose_name_plural = _('Vendas')
        ordering = ['-data_venda']
    
    def __str__(self):
        return f"Venda {self.numero_venda}"
    
    def save(self, *args, **kwargs):
        if not self.numero_venda:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.numero_venda = f"VND{timestamp}"
        super().save(*args, **kwargs)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name=_('Produto'))
    quantidade = models.DecimalField(_('Quantidade'), max_digits=8, decimal_places=2)
    preco_unitario = models.DecimalField(_('PreÃ§o UnitÃ¡rio'), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _('Item da Venda')
        verbose_name_plural = _('Itens da Venda')
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
